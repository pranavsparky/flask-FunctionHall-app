from flask import Flask, render_template, request, send_file
import os
from Generate_Bill import generate_bill

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    booking_data = {
        "name": request.form.get('name'),
        "pax": request.form.get('pax'),
        "mobile": request.form.get('mobile'),
        "event_type": request.form.get('event_type'),

        "checkin": request.form.get('checkin'),
        "checkout": request.form.get('checkout'),

        "room_needed": request.form.get('room_needed'),

        "double_rooms": request.form.get('double_rooms'),
        "double_extra": request.form.get('double_extra'),
        "double_ac": request.form.get('double_ac'),
        "double_rent": request.form.get('double_rent'),

        "triple_rooms": request.form.get('triple_rooms'),
        "triple_extra_bed": request.form.get('triple_extra_bed'),
        "triple_ac": request.form.get('triple_ac'),
        "triple_rent_per_room": request.form.get('triple_rent_per_room'),

        "function_rent": request.form.get('function_rent'),
        "cleaning_charges": request.form.get('cleaning_charges'),
        "security_charges": request.form.get('security_charges'),
        "electricity_charges": request.form.get('electricity_charges'),

        "advance": request.form.get('advance'),
        "advance_mode": request.form.get('advance_mode'),  # ✔ FIXED KEY

        "remarks": request.form.get('remarks')
    }

    filepath = generate_bill(booking_data)

    return send_file(filepath, as_attachment=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
