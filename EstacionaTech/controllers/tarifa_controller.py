from flask import Blueprint, render_template, request, redirect, url_for, flash
from EstacionaTech.models.tarifa import obter_tarifa, atualizar_tarifa

tarifa_bp = Blueprint('tarifa', __name__)

@tarifa_bp.route('/config_tarifas', methods=['GET', 'POST'])
def config_tarifas():
    if request.method == 'POST':
        valor_por_hora = request.form['valor_por_hora']
        tempo_tolerancia = request.form['tempo_tolerancia']

        try:
            atualizar_tarifa(valor_por_hora, tempo_tolerancia)
            flash('Tarifa atualizada com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao atualizar tarifa: {e}', 'error')

        return redirect(url_for('tarifa.config_tarifas'))

    tarifa = obter_tarifa()
    return render_template('config_tarifas.html', tarifa=tarifa)
