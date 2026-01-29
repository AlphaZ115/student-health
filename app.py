from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "health.db"


# ---------- DB CONNECT ----------
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ---------- INIT DATABASE ----------
def init_db():
    conn = get_db()
    with open("schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.close()


# ---------- HOME ----------
@app.route("/")
def home():
    return redirect(url_for("students"))


# ---------- STUDENTS LIST ----------
@app.route("/students")
def students():
    conn = get_db()
    rows = conn.execute("SELECT * FROM HocSinh").fetchall()
    conn.close()
    return render_template("students.html", students=rows)


# ---------- ADD STUDENT ----------
@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        ten = request.form["TenHS"]
        lop = request.form["Lop"]
        ngaysinh = request.form["NgaySinh"]

        conn = get_db()
        conn.execute(
            "INSERT INTO HocSinh (TenHS, Lop, NgaySinh) VALUES (?, ?, ?)",
            (ten, lop, ngaysinh),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("students"))

    return render_template("add_student.html")


# ---------- EDIT STUDENT ----------
@app.route("/students/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    conn = get_db()

    if request.method == "POST":
        ten = request.form["TenHS"]
        lop = request.form["Lop"]
        ngaysinh = request.form["NgaySinh"]

        conn.execute(
            "UPDATE HocSinh SET TenHS=?, Lop=?, NgaySinh=? WHERE MaHS=?",
            (ten, lop, ngaysinh, id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("students"))

    student = conn.execute("SELECT * FROM HocSinh WHERE MaHS=?", (id,)).fetchone()
    conn.close()
    return render_template("edit_student.html", student=student)


# ---------- DELETE STUDENT ----------
@app.route("/students/delete/<int:id>")
def delete_student(id):
    conn = get_db()
    conn.execute("DELETE FROM SucKhoe WHERE MaHS=?", (id,))
    conn.execute("DELETE FROM HocSinh WHERE MaHS=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("students"))


# ---------- HEALTH RECORDS ----------
@app.route("/health/<int:student_id>")
def health_records(student_id):
    conn = get_db()
    student = conn.execute(
        "SELECT * FROM HocSinh WHERE MaHS=?", (student_id,)
    ).fetchone()
    records = conn.execute(
        "SELECT * FROM SucKhoe WHERE MaHS=? ORDER BY NgayKham DESC", (student_id,)
    ).fetchall()
    conn.close()
    return render_template("health_records.html", student=student, records=records)


# ---------- ADD HEALTH RECORD ----------
@app.route("/health/add/<int:student_id>", methods=["GET", "POST"])
def add_health_record(student_id):
    conn = get_db()

    if request.method == "POST":
        chieucao = float(request.form["ChieuCao"])
        cannang = float(request.form["CanNang"])
        ngaykham = request.form["NgayKham"]

        conn.execute(
            "INSERT INTO SucKhoe (MaHS, ChieuCao, CanNang, NgayKham) VALUES (?, ?, ?, ?)",
            (student_id, chieucao, cannang, ngaykham),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("health_records", student_id=student_id))

    student = conn.execute(
        "SELECT * FROM HocSinh WHERE MaHS=?", (student_id,)
    ).fetchone()
    conn.close()
    return render_template("add_health_record.html", student=student)


# ---------- BMI ANALYSIS ----------
@app.route("/analysis/bmi")
def bmi_analysis():
    conn = get_db()
    query = """
        SELECT HocSinh.MaHS, HocSinh.TenHS, HocSinh.Lop,
               SucKhoe.ChieuCao, SucKhoe.CanNang, SucKhoe.NgayKham,
               (SucKhoe.CanNang / (SucKhoe.ChieuCao * SucKhoe.ChieuCao)) AS BMI
        FROM SucKhoe
        JOIN HocSinh ON SucKhoe.MaHS = HocSinh.MaHS
        WHERE BMI < 18.5 OR BMI > 25
        ORDER BY BMI
    """
    abnormal_records = conn.execute(query).fetchall()
    conn.close()
    return render_template("bmi_analysis.html", records=abnormal_records)


# ---------- MONTHLY STATISTICS ----------
@app.route("/analysis/monthly")
def monthly_stats():
    conn = get_db()
    query = """
        SELECT strftime('%Y-%m', NgayKham) AS Thang,
               COUNT(*) AS SoLan
        FROM SucKhoe
        GROUP BY Thang
        ORDER BY Thang DESC
    """
    stats = conn.execute(query).fetchall()
    conn.close()
    return render_template("monthly_stats.html", stats=stats)


# ---------- HEIGHT COMPARISON ----------
@app.route("/analysis/height")
def height_comparison():
    conn = get_db()
    query = """
        SELECT Lop,
               AVG(ChieuCao) AS CaoTB,
               COUNT(DISTINCT HocSinh.MaHS) AS SoHocSinh
        FROM SucKhoe
        JOIN HocSinh ON SucKhoe.MaHS = HocSinh.MaHS
        GROUP BY Lop
        ORDER BY Lop
    """
    stats = conn.execute(query).fetchall()
    conn.close()
    return render_template("height_comparison.html", stats=stats)


# ---------- RUN ----------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
