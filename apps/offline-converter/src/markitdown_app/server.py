from __future__ import annotations

import argparse
import io
import mimetypes
import os
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from uuid import uuid4

from flask import Flask, Response, jsonify, render_template, request, send_file
from markitdown import MarkItDown, StreamInfo
from markitdown._exceptions import FileConversionException, UnsupportedFormatException
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename


STATIC_ROOT = Path(__file__).resolve().parent / "static"
MAX_UPLOAD_BYTES = int(os.environ.get("MARKITDOWN_APP_MAX_UPLOAD_BYTES", 250 * 1024 * 1024))
MAX_UPLOAD_FILES = int(os.environ.get("MARKITDOWN_APP_MAX_UPLOAD_FILES", 50))
APP_DISPLAY_NAME = "PageMint Offline"


@dataclass(frozen=True)
class ConvertedFile:
    original_name: str
    output_name: str
    detected_extension: str | None
    detected_mimetype: str | None
    markdown: str


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(STATIC_ROOT),
        static_folder=str(STATIC_ROOT),
        static_url_path="/static",
    )
    app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES
    app.config["TRUSTED_HOSTS"] = ["127.0.0.1", "localhost"]

    @app.after_request
    def add_security_headers(response: Response) -> Response:
        response.headers["Cache-Control"] = "no-store"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; img-src 'self' data:; "
            "style-src 'self'; script-src 'self'; object-src 'none'; "
            "base-uri 'none'; frame-ancestors 'none'; form-action 'self'"
        )
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        return response

    @app.errorhandler(RequestEntityTooLarge)
    def upload_too_large(_error: RequestEntityTooLarge) -> tuple[Response, int]:
        limit_mb = MAX_UPLOAD_BYTES // (1024 * 1024)
        return jsonify({"error": f"Upload exceeds the {limit_mb} MB request limit."}), 413

    @app.get("/")
    def index() -> str:
        return render_template(
            "index.html",
            app_name=APP_DISPLAY_NAME,
            max_upload_mb=MAX_UPLOAD_BYTES // (1024 * 1024),
        )

    @app.get("/privacy")
    def privacy() -> str:
        return render_template("privacy.html", app_name=APP_DISPLAY_NAME)

    @app.post("/api/convert")
    def convert() -> Response:
        uploads = [file for file in request.files.getlist("files") if file.filename]
        upload_error = validate_uploads(uploads)
        if upload_error:
            return jsonify({"error": upload_error}), 400

        mode = request.form.get("mode", "combined")
        if mode not in {"combined", "separate"}:
            return jsonify({"error": "Mode must be either combined or separate."}), 400

        collection_name = clean_collection_name(request.form.get("collection_name"))

        try:
            converted = convert_uploads(uploads)
        except UnsupportedFormatException as exc:
            return jsonify({"error": str(exc)}), 415
        except FileConversionException as exc:
            return jsonify({"error": str(exc)}), 422
        except Exception as exc:
            return jsonify({"error": f"Conversion failed: {exc}"}), 500

        if mode == "separate":
            return send_file(
                build_zip(converted),
                mimetype="application/zip",
                as_attachment=True,
                download_name="pagemint-separate.zip",
            )

        return send_file(
            io.BytesIO(build_combined_markdown(converted, collection_name).encode("utf-8")),
            mimetype="text/markdown; charset=utf-8",
            as_attachment=True,
            download_name="pagemint-combined.md",
        )

    @app.post("/api/detect")
    def detect() -> Response:
        uploads = [file for file in request.files.getlist("files") if file.filename]
        upload_error = validate_uploads(uploads)
        if upload_error:
            return jsonify({"error": upload_error}), 400
        detections = []
        with tempfile.TemporaryDirectory(prefix="markitdown-app-") as tmp:
            tmpdir = Path(tmp)
            converter = MarkItDown(enable_plugins=False)
            for upload in uploads:
                path = save_upload(upload, tmpdir)
                detected = detect_file(converter, path)
                detections.append(
                    {
                        "name": upload.filename,
                        "extension": detected.extension,
                        "mimetype": detected.mimetype,
                        "charset": detected.charset,
                    }
                )
        return jsonify({"files": detections})

    return app


def validate_uploads(uploads: list[FileStorage]) -> str | None:
    if not uploads:
        return "Choose at least one file."
    if len(uploads) > MAX_UPLOAD_FILES:
        return f"Choose no more than {MAX_UPLOAD_FILES} files at a time."
    return None


def convert_uploads(uploads: Iterable[FileStorage]) -> list[ConvertedFile]:
    converted: list[ConvertedFile] = []
    with tempfile.TemporaryDirectory(prefix="markitdown-app-") as tmp:
        tmpdir = Path(tmp)
        converter = MarkItDown(enable_plugins=False)
        for upload in uploads:
            path = save_upload(upload, tmpdir)
            detected = detect_file(converter, path)
            result = converter.convert_local(path)
            converted.append(
                ConvertedFile(
                    original_name=upload.filename or path.name,
                    output_name=unique_markdown_name(upload.filename or path.name),
                    detected_extension=detected.extension,
                    detected_mimetype=detected.mimetype,
                    markdown=result.markdown,
                )
            )
    return converted


def save_upload(upload: FileStorage, tmpdir: Path) -> Path:
    safe_name = secure_filename(upload.filename or "")
    if not safe_name:
        safe_name = f"upload-{uuid4().hex}"
    path = tmpdir / safe_name
    upload.save(path)
    return path


def detect_file(converter: MarkItDown, path: Path) -> StreamInfo:
    base_guess = StreamInfo(
        local_path=str(path),
        filename=path.name,
        extension=path.suffix or None,
        mimetype=mimetypes.guess_type(path.name, strict=False)[0],
    )
    with path.open("rb") as file_stream:
        guesses = converter._get_stream_info_guesses(file_stream, base_guess=base_guess)
    return guesses[0] if guesses else base_guess


def build_combined_markdown(
    files: list[ConvertedFile], collection_name: str | None = None
) -> str:
    title = collection_name or "PageMint Collection"
    intro = f"# {title}\n\n_Converted locally by {APP_DISPLAY_NAME}. Files processed: {len(files)}._"
    sections = [intro]
    for item in files:
        detected = " / ".join(
            part for part in (item.detected_extension, item.detected_mimetype) if part
        )
        suffix = f"\n\n_Detected: {detected}_" if detected else ""
        sections.append(f"# {item.original_name}{suffix}\n\n{item.markdown.strip()}")
    return "\n\n---\n\n".join(sections).strip() + "\n"


def build_zip(files: list[ConvertedFile]) -> io.BytesIO:
    archive = io.BytesIO()
    used_names: dict[str, int] = {}
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("_pagemint-summary.md", build_summary_markdown(files))
        for item in files:
            name = dedupe_name(item.output_name, used_names)
            zip_file.writestr(name, item.markdown.strip() + "\n")
    archive.seek(0)
    return archive


def build_summary_markdown(files: list[ConvertedFile]) -> str:
    lines = [
        "# PageMint Conversion Summary",
        "",
        f"Converted locally by {APP_DISPLAY_NAME}.",
        "",
        "| File | Detected format | Output |",
        "| --- | --- | --- |",
    ]
    for item in files:
        detected = " / ".join(
            part for part in (item.detected_extension, item.detected_mimetype) if part
        )
        lines.append(
            f"| {escape_table_cell(item.original_name)} | {escape_table_cell(detected or 'unknown')} | {escape_table_cell(item.output_name)} |"
        )
    return "\n".join(lines) + "\n"


def escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|")


def clean_collection_name(value: str | None) -> str | None:
    if value is None:
        return None
    value = " ".join(value.split())
    return value[:80] or None


def unique_markdown_name(filename: str) -> str:
    stem = Path(filename).stem or "converted"
    return f"{secure_filename(stem) or 'converted'}.md"


def dedupe_name(name: str, used_names: dict[str, int]) -> str:
    if name not in used_names:
        used_names[name] = 1
        return name
    used_names[name] += 1
    path = Path(name)
    return f"{path.stem}-{used_names[name]}{path.suffix}"


def main() -> None:
    parser = argparse.ArgumentParser(description=f"Run {APP_DISPLAY_NAME}.")
    parser.add_argument("--port", default=8765, type=int)
    args = parser.parse_args()

    app = create_app()
    from waitress import serve

    serve(app, host="127.0.0.1", port=args.port)


if __name__ == "__main__":
    main()
