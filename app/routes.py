from flask import Blueprint, render_template, request, redirect, url_for, abort, jsonify
from app import db
from app.models import Notice, CATEGORIES

main = Blueprint("main", __name__)


# ── Página principal: lista de anuncios ───────────────────────
@main.route("/")
def index():
    category = request.args.get("category", "")
    query = Notice.query.order_by(Notice.created_at.desc())
    if category and category in CATEGORIES:
        query = query.filter_by(category=category)
    notices = query.all()
    return render_template(
        "index.html",
        notices=notices,
        categories=CATEGORIES,
        selected=category,
    )


# ── Formulario para crear un anuncio ─────────────────────────
@main.route("/new", methods=["GET"])
def new_notice_form():
    return render_template("new.html", categories=CATEGORIES)


@main.route("/new", methods=["POST"])
def new_notice_submit():
    title    = request.form.get("title", "").strip()
    content  = request.form.get("content", "").strip()
    category = request.form.get("category", "General")
    author   = request.form.get("author", "").strip()

    errors = []
    if not title:
        errors.append("El título es obligatorio.")
    if not content:
        errors.append("El contenido es obligatorio.")
    if not author:
        errors.append("El nombre del autor es obligatorio.")
    if category not in CATEGORIES:
        errors.append("Categoría no válida.")

    if errors:
        return render_template(
            "new.html",
            categories=CATEGORIES,
            errors=errors,
            form_data=request.form,
        ), 400

    notice = Notice(
        title=title,
        content=content,
        category=category,
        author=author,
    )
    db.session.add(notice)
    db.session.commit()
    return redirect(url_for("main.index"))


# ── Detalle de un anuncio ─────────────────────────────────────
@main.route("/notice/<int:notice_id>")
def notice_detail(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    return render_template("notice.html", notice=notice)


# ── Eliminar un anuncio ───────────────────────────────────────
@main.route("/notice/<int:notice_id>/delete", methods=["POST"])
def notice_delete(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    db.session.delete(notice)
    db.session.commit()
    return redirect(url_for("main.index"))


# ── Health check ──────────────────────────────────────────────
@main.route("/health")
def health():
    return jsonify({"status": "ok", "version": "1.0.0"})
