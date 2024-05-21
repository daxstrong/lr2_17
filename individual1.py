#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import sys
from datetime import datetime


def exit_program():
    """
    Выход из программы.
    """
    sys.exit()


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
    print(line)
    print(f"| {'Фамилия':^25} | {'Имя':^15} | {'Дата рождения':^25} |")

    for person in people:
        print(line)
        print(f"| {person['фамилия']:^25} | {person['имя']:^15} | {person['дата рождения'].strftime('%d.%m.%Y'):^25} |")
    print(line)


def select_people_by_month(people, month_to_search):
    """
    Вывод людей с днем рождения в указанном месяце.
    """
    found = False

    print(f"Люди с днем рождения в месяце {month_to_search}:")
    for person in people:
        if person['дата рождения'].month == month_to_search:
            print(
                f"Фамилия: {person['фамилия']}, Имя: {person['имя']}, Номер телефона: {person['номер телефона']}, Дата рождения: {person['дата рождения'].strftime('%d.%m.%Y')}")
            found = True

    if not found:
        print("Нет людей с днем рождения в указанном месяце.")


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


def main(command_line=None):
    """Основная функция управления программой."""

    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="Имя файла для данных"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("people")
    parser.add_argument(
        "--version", action="version", version="%(prog)s 1.0.0"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления человека.
    add = subparsers.add_parser(
        "add", parents=[file_parser], help="Добавить информацию о человеке"
    )
    add.add_argument(
        "-l", "--last_name", action="store", required=True, help="Фамилия"
    )
    add.add_argument(
        "-f", "--first_name", action="store", required=True, help="Имя"
    )
    add.add_argument(
        "-p", "--phone_number", action="store", required=True, help="Номер телефона"
    )
    add.add_argument(
        "-b", "--birthdate", action="store", required=True, help="Дата рождения (в формате ДД.ММ.ГГГГ)"
    )

    # Создать субпарсер для вывода всех людей.
    _ = subparsers.add_parser(
        "list",
        parents=[file_parser],
        help="Вывести список всех людей"
    )

    # Создать субпарсер для выбора людей по месяцу рождения.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Вывести людей с днем рождения в указанном месяце"
    )
    select.add_argument(
        "-m",
        "--month",
        action="store",
        type=int,
        required=True,
        help="Месяц (число от 1 до 12)"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить всех людей из файла, если файл существует.
    changed_file = False
    if os.path.exists(args.filename):
        people = load_people(args.filename)
    else:
        people = []

    # Добавить человека.
    if args.command == "add":
        people = add_person(
            people,
            args.last_name,
            args.first_name,
            args.phone_number,
            args.birthdate
        )
        changed_file = True

    # Вывести всех людей.
    elif args.command == "list":
        list_people(people)

    # Выбрать людей по месяцу рождения.
    elif args.command == "select":
        select_people_by_month(people, args.month)

    else:
        print(f"Неизвестная команда {args.command}", file=sys.stderr)

    # Сохранить данные в файл, если список людей был изменен.
    if changed_file:
        save_people(args.filename, people)


if __name__ == '__main__':
    main()
