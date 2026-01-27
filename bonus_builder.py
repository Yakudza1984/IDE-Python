import streamlit as st
import yaml
from datetime import date

st.set_page_config(page_title="Bonus Constructor", layout="centered")

st.title("🧩 Конструктор бонусов (MVP)")
st.caption("Соберите правило бонуса без программирования")

# -----------------------------
# Основная информация
# -----------------------------
st.header("1. Общая информация")

bonus_name = st.text_input("Название бонуса", "Quarterly Retro Bonus")

# -----------------------------
# Scope
# -----------------------------
st.header("2. Область действия")

supplier = st.text_input("Поставщик", "ABC Foods")
category = st.multiselect("Категории", ["Напитки", "Бакалея", "Табак"])

# -----------------------------
# Период
# -----------------------------
st.header("3. Период")

calc_period = st.selectbox("Период расчёта", ["month", "quarter", "year"])
valid_from = st.date_input("Действует с", date(2026, 1, 1))
valid_to = st.date_input("Действует по", date(2026, 12, 31))

# -----------------------------
# База расчёта
# -----------------------------
st.header("4. База расчёта")

base = st.selectbox(
    "От чего считаем",
    ["turnover", "promo_turnover", "quantity", "margin", "plan_execution", "fixed"]
)

# -----------------------------
# Условие
# -----------------------------
st.header("5. Условие начисления (опционально)")

use_condition = st.checkbox("Есть условие")

if use_condition:
    cond_metric = st.selectbox("Метрика", ["turnover", "plan_execution"])
    cond_operator = st.selectbox("Оператор", [">=", ">", "<=", "<", "="])
    cond_value = st.number_input("Значение", min_value=0.0, value=1.0)

# -----------------------------
# Формула
# -----------------------------
st.header("6. Формула расчёта")

formula_type = st.radio(
    "Тип формулы",
    ["percent", "fixed", "tiered_percent", "conditional"]
)

formula = {}

if formula_type == "percent":
    rate = st.number_input("Процент (%)", min_value=0.0, value=3.0)
    formula = {"type": "percent", "value": rate}

elif formula_type == "fixed":
    amount = st.number_input("Сумма", min_value=0.0, value=3_000_000)
    formula = {"type": "fixed", "value": amount}

elif formula_type == "tiered_percent":
    st.caption("Ступени")
    tiers = []
    for i in range(3):
        col1, col2 = st.columns(2)
        with col1:
            from_value = st.number_input(f"От (ступень {i+1})", min_value=0.0, key=f"from_{i}")
        with col2:
            tier_rate = st.number_input(f"% (ступень {i+1})", min_value=0.0, key=f"rate_{i}")
        if tier_rate > 0:
            tiers.append({"from": from_value, "value": tier_rate})

    formula = {"type": "tiered_percent", "tiers": tiers}

elif formula_type == "conditional":
    st.caption("Условие")
    if_metric = st.selectbox("Метрика", ["plan_execution"])
    if_value = st.number_input("Значение условия", value=1.1)

    col1, col2 = st.columns(2)
    with col1:
        then_rate = st.number_input("Если ДА (%)", value=5.0)
    with col2:
        else_rate = st.number_input("Если НЕТ (%)", value=3.0)

    formula = {
        "type": "conditional",
        "if": {
            "metric": if_metric,
            "operator": ">=",
            "value": if_value
        },
        "then": {"type": "percent", "value": then_rate},
        "else": {"type": "percent", "value": else_rate}
    }

# -----------------------------
# Исключения
# -----------------------------
st.header("7. Исключения")

exclude_categories = st.multiselect("Исключить категории", ["Табак", "Алкоголь"])

# -----------------------------
# Сбор DSL
# -----------------------------
bonus_dsl = {
    "bonus": bonus_name,
    "scope": {
        "supplier": supplier,
        **({"category": category} if category else {})
    },
    "period": {
        "valid_from": str(valid_from),
        "valid_to": str(valid_to),
        "calculation": calc_period
    },
    "base": base,
    "formula": formula
}

if use_condition:
    bonus_dsl["condition"] = {
        "metric": cond_metric,
        "operator": cond_operator,
        "value": cond_value
    }

if exclude_categories:
    bonus_dsl["exclude"] = {"category": exclude_categories}

# -----------------------------
# Предпросмотр
# -----------------------------
st.header("8. Предпросмотр")

st.subheader("DSL (YAML)")
st.code(yaml.dump(bonus_dsl, allow_unicode=True, sort_keys=False), language="yaml")

st.subheader("Как считается (человечески)")
description = f"Бонус «{bonus_name}»: "

if use_condition:
    description += f"если {cond_metric} {cond_operator} {cond_value}, "

if formula_type == "percent":
    description += f"начисляется {rate}% от {base}."
elif formula_type == "fixed":
    description += f"начисляется фиксированная сумма {amount}."
elif formula_type == "tiered_percent":
    description += "применяются ступени процентов от оборота."
elif formula_type == "conditional":
    description += f"{then_rate}% при выполнении условия, иначе {else_rate}%."

st.info(description)