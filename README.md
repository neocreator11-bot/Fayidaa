# Fayda Telegram Bot — Railway Starter

This project is a **development scaffold**, not a production Fayda integration. The Telegram UI and custom Flask webpage are included. OIDC is disabled by default, and the callback intentionally fails closed until the official token exchange and JWT validation are implemented and tested.

## Included
- Telegram `/start` and `/help` commands
- Custom English verification webpage
- OIDC authorization redirect scaffold with `state`, `nonce`, and PKCE S256
- Health endpoint (`/health`)
- Clearly marked development PDF receipt helper
- Railway deployment configuration

## Not yet implemented
- Token endpoint exchange and client-assertion signing
- Signature and claims validation for ID token / UserInfo JWT
- Validated association between Telegram user and browser session
- Delivery of a receipt to Telegram after validated authentication
- Retrieval of any official identity document (requires an authorized Fayda document API)

**Do not set `OIDC_ENABLED=true` until those missing checks are implemented and tested against official current documentation.** Merely returning from the authorization endpoint is not proof of identity verification.

## Local testing
1. Use Python 3.11 or newer.
2. Create a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Set `BOT_TOKEN`, `FLASK_SECRET_KEY`, and `PUBLIC_BASE_URL`.
5. Run the web service with `python web.py`.
6. Run the bot separately with `python bot.py`.

The web service runs on port 8080 by default. The bot uses polling.

## Railway deployment
Create a Railway project from this repository.

### Web service
- Start command: `gunicorn --workers 2 --bind 0.0.0.0:$PORT web:app`
- Add a public domain.
- Set `FLASK_SECRET_KEY` to a long random value.
- Set `PUBLIC_BASE_URL` to the public domain.
- Set `REDIRECT_URI` to `https://YOUR-DOMAIN/callback`.
- Keep `OIDC_ENABLED=false` during initial deployment.

### Bot service
- Start command: `python bot.py`
- Set `BOT_TOKEN` in the service Variables.
- Set `PUBLIC_BASE_URL` to the web service's public domain.

Railway may use a Procfile for service start commands; configure each service's start command explicitly if needed.

## Security checklist before live authentication
- Obtain/confirm authorized client credentials and exact redirect URI registration.
- Keep private keys and bot tokens in Railway Variables, never commit them.
- Implement client assertion exactly as the provider requires.
- Exchange code using `code_verifier`.
- Validate ID-token signature, issuer, audience, expiration, and nonce.
- Validate signed UserInfo JWT using the provider's official keys and required claims.
- Use short-lived, one-time state/session data and secure cookies.
- Do not request, collect, log, or store a user's Fayda OTP.
- Minimize identity data; do not log tokens or FAN.
- Confirm the legal/technical availability of an official document endpoint before offering identity-document downloads.
- Use HTTPS and test with sandbox personas only.

## Privacy note
Do not put real FANs, OTPs, identity documents, private keys, or production tokens into source code, logs, or Telegram messages.
