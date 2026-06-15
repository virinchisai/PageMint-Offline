from __future__ import annotations

import io
import zipfile

from markitdown_app.server import build_combined_markdown, build_zip, ConvertedFile, create_app


def converted_file(name: str, markdown: str = "hello") -> ConvertedFile:
    return ConvertedFile(
        original_name=name,
        output_name=f"{name}.md",
        detected_extension=".txt",
        detected_mimetype="text/plain",
        markdown=markdown,
    )


def test_combined_markdown_includes_each_file_heading() -> None:
    markdown = build_combined_markdown(
        [
            converted_file("first.txt", "First body"),
            converted_file("second.txt", "Second body"),
        ],
        "Client Archive",
    )

    assert "# Client Archive" in markdown
    assert "Converted locally by PageMint Offline" in markdown
    assert "# first.txt" in markdown
    assert "# second.txt" in markdown
    assert "_Detected: .txt / text/plain_" in markdown
    assert "\n\n---\n\n" in markdown


def test_zip_dedupes_output_names() -> None:
    archive = build_zip(
        [
            converted_file("same", "One"),
            converted_file("same", "Two"),
        ]
    )

    with zipfile.ZipFile(archive) as zip_file:
        assert zip_file.namelist() == ["_pagemint-summary.md", "same.md", "same-2.md"]
        assert "PageMint Conversion Summary" in zip_file.read(
            "_pagemint-summary.md"
        ).decode("utf-8")
        assert zip_file.read("same.md").decode("utf-8") == "One\n"


def test_convert_endpoint_returns_markdown_attachment() -> None:
    app = create_app()
    client = app.test_client()

    response = client.post(
        "/api/convert",
        data={
            "mode": "combined",
            "collection_name": "Mobile upload",
            "files": (io.BytesIO(b"plain text"), "sample.txt"),
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert response.mimetype == "text/markdown"
    assert b"# Mobile upload" in response.data
    assert b"# sample.txt" in response.data
    assert b"plain text" in response.data


def test_requests_reject_untrusted_hosts() -> None:
    client = create_app().test_client()

    response = client.get("/", headers={"Host": "attacker.example"})

    assert response.status_code == 400


def test_responses_include_security_headers() -> None:
    client = create_app().test_client()

    response = client.get("/")

    assert response.headers["Cache-Control"] == "no-store"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "frame-ancestors 'none'" in response.headers["Content-Security-Policy"]


def test_detect_requires_at_least_one_file() -> None:
    client = create_app().test_client()

    response = client.post("/api/detect")

    assert response.status_code == 400
    assert response.get_json() == {"error": "Choose at least one file."}


def test_convert_rejects_too_many_files(monkeypatch) -> None:
    monkeypatch.setattr("markitdown_app.server.MAX_UPLOAD_FILES", 1)
    client = create_app().test_client()

    response = client.post(
        "/api/convert",
        data={
            "mode": "combined",
            "files": [
                (io.BytesIO(b"one"), "one.txt"),
                (io.BytesIO(b"two"), "two.txt"),
            ],
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Choose no more than 1 files at a time."}
