from flask import Blueprint, render_template, request, redirect, url_for, flash
from EstacionaTech.models.tarifa import obter_tarifa, atualizar_tarifa

tarifa_bp = Blueprint('tarifa', __name__, template_folder='../templates')

@tarifa_bp.route('/config_tarifas', methods=['GET', 'POST'])
def config_tarifas():
    if request.method == 'POST':
        try:
            valor_por_hora = float(request.form['valor_por_hora'])  # Convertendo para float
            tempo_tolerancia = int(request.form['tempo_tolerancia'])  # Convertendo para int
            
            atualizar_tarifa(valor_por_hora, tempo_tolerancia)
            flash('Tarifa atualizada com sucesso!', 'success')
        except ValueError:
            flash('Erro: Valores inválidos! Insira um número válido.', 'error')
        except Exception as e:
            flash(f'Erro ao atualizar tarifa: {e}', 'error')

        return redirect(url_for('tarifa.config_tarifas'))

    tarifa = obter_tarifa()
    return render_template('config_tarifas.html', tarifa=tarifa)
