# type_of: 1 - Múltipla escolha, 2 - Verdadeiro ou falso, 3 - Numérica


from dateutil import parser

_d = parser.parse


questions = [
    {
        "title": "Qual a capital do Brasil?", "type_of": 1, "answer": "Brasília", "json_alternatives": '{"a":"Sao Paulo", "b": "Rio de Janeiro","c": "Brasilia", "d":"Belo Horizonte"}', "answer": 3, "comments": "Comentário sobre a questão"
    },
             
    {
        "title":'Qual é a capital da França?',
        "json_alternatives":'{"a": "Londres", "b": "Paris", "c": "Roma"}',
        "answer":2
        },
    
    {
        "title":'Qual é a capital da Alemanha?',
        "json_alternatives":'{"a": "Berlim", "b": "Paris", "c": "Roma"}',
        "answer":1
        },

    {   
        "title":'Qual é a capital da Itália?',
        "json_alternatives":'{"a": "Londres", "b": "Paris", "c": "Roma"}',
        "answer":3
        },
    {
        "title":'Qual é a capital da Espanha?',
        "json_alternatives":'{"a": "Londres", "b": "Madrid", "c": "Roma"}',
        "answer":2
    },
    {
        "title":'Responda a questão:',
        "json_alternatives": 'Qual o valor de x, sabendo que x+1 = 10?',
        "answer": 9
    },
    {
        "title":'Responda a questão:',
        "json_alternatives": 'Qual o valor de x, sabendo que x+2 = 10?',
        "answer": 8
    },
    {
        "title":'Julgue as afirmações como verdadeiro (V) ou falso (F)',
        "json_alternatives": '{"a": "A Terra é plana", "b": "A Terra é redonda", "c": "A Terra é quadrada", "d": "A Terra é cúbica", "e": "A Terra é triangular", "f": "A Terra é hexagonal", "g": "A Terra é pentagonal", "h": "A Terra é octogonal", "i": "A Terra é heptagonal", "j": "A Terra é esférica"}',
        #"answer": '{"a": "F", "b": "V", "c": "F", "d": "F", "e": "F", "f": "F", "g": "F", "h": "F", "i": "F", "j": "V"}',
        "answer": '{"a": 0, "b": 1, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0, "j": 1}'
    }
    ]


exams = [
    {
        "title": "Prova de Geografia", "qntityOfQuestions": 3, "punctuation": 10,  "comments": "Múltipla escolha: Marque a alternativa correta"},
    {
        "title": "Prova de Matemática", "qntityOfQuestions": 3, "punctuation": 10,  "comments": "Respostas em inteiros"},
    {
        "title": "Prova de História", "qntityOfQuestions": 3, "punctuation": 10,  "comments": "Verdadeiro ou falso: Marque V ou F"}
    
    ]



pwd_hash =  "$2b$12$QLpUyPzW8PF6Kidk/fMXM.AQQSCI7UK7OsUr4k.2qVAbPq7yPdrhy"   # bcrypt.generate_password_hash("asdasdasd")
pwd_hash3 = "$2b$12$DNf./WDisJfVGbw2TFlageeyvdYUES4B.H2SBLEdjjyfBk9cx8xqa"   # bcrypt.generate_password_hash("asdfg")

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
pwd_hash2 = bcrypt.generate_password_hash("asdfg")

users = [
    # {"username": "admin", "email": "1@d.m", "pwd": pwd_hash},
    # {"username": "admin2", "email": "2@d.m", "pwd": pwd_hash},
    
    {"name": "Ester", "username": "ester", "email": "ester@unb.br", "pwd": pwd_hash2, "is_student": True},
    {"name": "Pedro", "username": "pedro", "email": "pedro@unb.br", "pwd": pwd_hash2, "is_student": False},
    
    ]



