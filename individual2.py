#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import json
import os
from datetime import datetime


def add_person(people, last_name, first_name, phone_number, birthdate_str):
    """
    Добавление информации о человеке.
    """
    birthdate = datetime.strptime(birthdate_str, "%d.%m.%Y")

    person = {
        'фамилия': last_name,
        'имя': first_name,
        'номер телефона': phone_number,
        'дата рождения': birthdate,
    }

    people.append(person)
    people.sort(key=lambda x: x['фамилия'])
    return people


def list_people(people):
    """
    Вывод списка всех людей.
    """
    line = f'+-{"-" * 25}-+-{"-" * 15}-+-{"-" * 25}-+'
    click.echo(line)
    click.echo(f"| {'Фамилия':^25} | {'Имя':^15} | {'Дата рождения':^25} |")

    for person in people:
        click.echo(line)
        click.echo(
            f"| {person['фамилия']:^25} | {person['имя']:^15} | {person['дата рождения'].strftime('%d.%m.%Y'):^25} |")
    click.echo(line)


def select_people_by_month(people, month_to_search):
    """
    Вывод людей с днем рождения в указанном месяце.
    """
    found = False

    click.echo(f"Люди с днем рождения в месяце {month_to_search}:")
    for person in people:
        if person['дата рождения'].month == month_to_search:
            click.echo(
                f"Фамилия: {person['фамилия']}, Имя: {person['имя']}, Номер телефона: {person['номер телефона']}, Дата рождения: {person['дата рождения'].strftime('%d.%m.%Y')}")
            found = True

    if not found:
        click.echo("Нет людей с днем рождения в указанном месяце.")


def save_people(file_name, people):
    """
    Сохранить всех людей в файл JSON.
    """
    # Преобразуем объекты datetime в строки
    for person in people:
        person['дата рождения'] = person['дата рождения'].strftime('%d.%m.%Y')

    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(people, fout, ensure_ascii=False, indent=4)


def load_people(file_name):
    """
    Загрузить всех людей из файла JSON.
    """
    try:
        with open(file_name, "r", encoding="utf-8") as fin:
            people_data = json.load(fin)
            for person in people_data:
                person['дата рождения'] = datetime.strptime(person['дата рождения'], '%d.%m.%Y')
            return people_data
    except FileNotFoundError:
        return []


@click.group()
def cli():
    """Список команд для управления информацией о людях."""
    pass


@cli.command()
@click.argument('filename', type=click.Path())
@click.option('-l', '--last_name', prompt='Фамилия', help='Фамилия')
@click.option('-f', '--first_name', prompt='Имя', help='Имя')
@click.option('-p', '--phone_number', prompt='Номер телефона', help='Номер телефона')
@click.option('-b', '--birthdate', prompt='Дата рождения (ДД.ММ.ГГГГ)', help='Дата рождения (в формате ДД.ММ.ГГГГ)')
def add(filename, last_name, first_name, phone_number, birthdate):
    """Добавить информацию о новом человеке."""
    if os.path.exists(filename):
        people = load_people(filename)
    else:
        people = []

    people = add_person(people, last_name, first_name, phone_number, birthdate)
    save_people(filename, people)


@cli.command()
@click.argument('filename', type=click.Path())
def list(filename):
    """Вывести список всех людей."""
    if os.path.exists(filename):
        people = load_people(filename)
        list_people(people)
    else:
        click.echo("Файл не найден.")


@cli.command()
@click.argument('filename', type=click.Path())
@click.option('-m', '--month', prompt='Месяц', type=int, help='Месяц (число от 1 до 12)')
def select(filename, month):
    """Вывести людей с днем рождения в указанном месяце."""
    if os.path.exists(filename):
        people = load_people(filename)
        select_people_by_month(people, month)
    else:
        click.echo("Файл не найден.")


if __name__ == '__main__':
    cli()
