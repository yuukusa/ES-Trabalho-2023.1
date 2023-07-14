# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)

from dateutil import parser

_d = parser.parse


questions = [
    {
        "title": "Qual a capital do Brasil?", "type_of": 1, "answer": "Brasília", "alternatives": '{"Sao Paulo", "Rio de Janeiro", "Brasilia", "Belo Horizonte"}', "answer": 3, "comments": "Comentário sobre a questão"
    },
             
    {
        "title":'Qual é a capital da França?',
        "alternatives":'{"a": "Londres", "b": "Paris", "c": "Roma"}',
        "answer":2
        },
    
    {
        "title":'Qual é a capital da Alemanha?',
        "alternatives":'{"a": "Berlim", "b": "Paris", "c": "Roma"}',
        "answer":1
        }
    ]


exams = [
    {
        "title": "Prova de Geografia", "quantity": 3, "punctuation": 10,  "comments": "Comentário sobre a prova"},
    {
        "title": "Prova de Matemática", "quantity": 3, "punctuation": 10,  "comments": "Comentário sobre a prova"},
    {
        "title": "Prova de História", "quantity": 3, "punctuation": 10,  "comments": "Comentário sobre a prova"}
    
    ]



pwd_hash = "$2b$12$QLpUyPzW8PF6Kidk/fMXM.AQQSCI7UK7OsUr4k.2qVAbPq7yPdrhy"
users = [
    {"username": "admin", "email": "1@d.m", "pwd": pwd_hash},
    {"username": "admin2", "email": "2@d.m", "pwd": pwd_hash},
    
    {"username": "ester", "email": "ester@unb.br", "senha": "asdfg", "is_student": True},
    {"username": "pedro", "email": "pedro@unb.br", "senha": "asdfg", "is_student": False},
    
    {"username": "ana", "email": "3@d.m", "pwd": pwd_hash},
    {"username": "bob", "email": "4@d.m", "pwd": pwd_hash},
    {"username": "carol", "email": "5@d.m", "pwd": pwd_hash},
]



