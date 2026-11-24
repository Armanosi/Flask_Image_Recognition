
"""Security tests for CSRF protection."""

from app import app


def test_prediction_rejects_missing_csrf_token():
    """POST requests without a CSRF token must be rejected."""
    with app.test_client() as client:
        with app.test_request_context():
            original_setting = app.config.get(
                "WTF_CSRF_ENABLED", True
            )

        try:
            app.config["WTF_CSRF_ENABLED"] = True

            response = client.post(
                "/prediction",
                data={}
            )

            assert response.status_code == 400
        finally:
            app.config["WTF_CSRF_ENABLED"] = original_setting
