import os
import sys
import django

# Django muhitini sozlash
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import Category, Unit, Product


def populate():
    print("O'lchov birliklarini yaratish...")
    units_data = [
        {"name": "Metr kub", "short_name": "m³"},
        {"name": "Dona", "short_name": "dona"},
        {"name": "Metr", "short_name": "metr"},
        {"name": "Qop (50kg)", "short_name": "qop"},
        {"name": "List", "short_name": "list"},
        {"name": "Kilogramm", "short_name": "kg"},
        {"name": "Bankasi", "short_name": "banka"},
    ]
    units = {}
    for u in units_data:
        unit_obj, _ = Unit.objects.get_or_create(
            short_name=u["short_name"],
            defaults={"name": u["name"]}
        )
        units[u["short_name"]] = unit_obj

    print("Kategoriyalar va mahsulotlarni yaratish...")
    categories_data = [
        {
            "name": "Yog'och va Taxtalar",
            "icon": "🪵",
            "order": 1,
            "products": [
                {
                    "name": "Qarag'ay taxtasi (Rossiya) 50x150x6000",
                    "description": "1-navli Rossiya qarag'ay taxtasi. Qurilish, tomlar va pollar uchun a'lo sifatli.",
                    "price": 3400000.00,
                    "unit": units["m³"]
                },
                {
                    "name": "Qarag'ay taxtasi 25x100x6000",
                    "description": "Obreshyotka va yordamchi qurilish ishlari uchun quruq taxta.",
                    "price": 3200000.00,
                    "unit": units["m³"]
                },
                {
                    "name": "Qarag'ay Brusi 100x100x6000",
                    "description": "Mustahkam ustunlar va karkaslar uchun yuqori sifatli brus.",
                    "price": 3500000.00,
                    "unit": units["m³"]
                },
                {
                    "name": "Reyka 20x40x3000",
                    "description": "Shift va devor montaj ishlari uchun silliqlangan reyka.",
                    "price": 6000.00,
                    "unit": units["metr"]
                },
                {
                    "name": "Fanera (Finiy) 1525x1525x18mm",
                    "description": "Suvga chidamli va mustahkam fanera listi. Pol va mebellar uchun.",
                    "price": 185000.00,
                    "unit": units["list"]
                },
                {
                    "name": "Laminatsiyalangan Fanera (Opalubka uchun) 18mm",
                    "description": "Monolit quyish uchun maxsus silliq suvga chidamli fanera.",
                    "price": 320000.00,
                    "unit": units["list"]
                },
            ]
        },
        {
            "name": "G'isht va Bloklar",
            "icon": "🧱",
            "order": 2,
            "products": [
                {
                    "name": "Pishiq g'isht (Standart M-150)",
                    "description": "Pishgan qizil g'isht, poydevor va asosiy devorlar uchun.",
                    "price": 1200.00,
                    "unit": units["dona"]
                },
                {
                    "name": "Gazoblok 600x300x200 D500",
                    "description": "Issiqlikni a'lo darajada saqlovchi va yengil gazobeton bloki.",
                    "price": 26000.00,
                    "unit": units["dona"]
                },
                {
                    "name": "Shlakoblok 390x190x190",
                    "description": "Devor va to'siqlar qurish uchun presslangan pishiq blok.",
                    "price": 4500.00,
                    "unit": units["dona"]
                },
                {
                    "name": "Peno blok 600x300x100 (To'siq uchun)",
                    "description": "Xonalararo to'siq devorlari uchun yengil penoblok.",
                    "price": 15000.00,
                    "unit": units["dona"]
                }
            ]
        },
        {
            "name": "Sement va Qorishmalar",
            "icon": "🏗",
            "order": 3,
            "products": [
                {
                    "name": "Qizilqum Sement M-400 (50 kg)",
                    "description": "Yuqori sifatli portlandsement. Barcha turdagi beton ishlari uchun.",
                    "price": 48000.00,
                    "unit": units["qop"]
                },
                {
                    "name": "Olmaliq Sement M-500 (50 kg)",
                    "description": "Katta yuk ko'taruvchi monolit va poydevorlar uchun baquvvat sement.",
                    "price": 54000.00,
                    "unit": units["qop"]
                },
                {
                    "name": "Rotband Gipsli Suvoq (30 kg)",
                    "description": "Ichki devorlarni tekislash uchun sifatli gips qorishmasi.",
                    "price": 42000.00,
                    "unit": units["qop"]
                },
                {
                    "name": "Kafel Yelimi Ceresit CM-11 (25 kg)",
                    "description": "Kafel va granit plitalarini yopishtirish uchun mustahkam kley.",
                    "price": 38000.00,
                    "unit": units["qop"]
                }
            ]
        },
        {
            "name": "Metall va Armatura",
            "icon": "⚙️",
            "order": 4,
            "products": [
                {
                    "name": "Armatura A500C Ø 12 mm (Bekobod)",
                    "description": "Sifatli issiq prokatli po'lat armatura, 12 metrli.",
                    "price": 9800.00,
                    "unit": units["metr"]
                },
                {
                    "name": "Armatura A500C Ø 14 mm",
                    "description": "Monolit poydevorlar uchun yuqori mustahkamlikdagi armatura.",
                    "price": 13500.00,
                    "unit": units["metr"]
                },
                {
                    "name": "Profil quvur 40x40x2.0 mm",
                    "description": "Darvoza, panjara va tom karkaslari uchun po'lat profil.",
                    "price": 24000.00,
                    "unit": units["metr"]
                },
                {
                    "name": "Bog'lovchi Katanka Sim Ø 1.2 mm",
                    "description": "Armatura karkaslarini bog'lash uchun yumshoq sim.",
                    "price": 12000.00,
                    "unit": units["kg"]
                }
            ]
        },
        {
            "name": "Tom Yopish Materiallari",
            "icon": "🏠",
            "order": 5,
            "products": [
                {
                    "name": "Profmastil 0.45 mm (Shokolad/Qizil)",
                    "description": "Zanglamaydigan va uzoq xizmat qiluvchi polimer qoplamali profnastil.",
                    "price": 48000.00,
                    "unit": units["metr"]
                },
                {
                    "name": "Klassik 8-to'lqinli Shifer",
                    "description": "Standart sifatli asbest shifer tomlar uchun.",
                    "price": 45000.00,
                    "unit": units["list"]
                },
                {
                    "name": "Bikrost / Ruberoid Gidroizolyatsiya",
                    "description": "Tom va poydevorlarni namlikdan himoya qiluvchi qoplama.",
                    "price": 140000.00,
                    "unit": units["list"]
                }
            ]
        },
        {
            "name": "Bo'yoqlar va Laklar",
            "icon": "🎨",
            "order": 6,
            "products": [
                {
                    "name": "Fasor Vodomulsiya (Oq, 20 kg)",
                    "description": "Ichki va tashqi devorlar uchun yuviladigan matoviy bo'yoq.",
                    "price": 160000.00,
                    "unit": units["banka"]
                },
                {
                    "name": "Yog'och Laki (Yaltiroq, 3 kg)",
                    "description": "Taxta va yog'och mahsulotlarini quyosh va namdan asrovchi lak.",
                    "price": 75000.00,
                    "unit": units["banka"]
                },
                {
                    "name": "Gruntovka Glubokogo Proniknoveniya (10 L)",
                    "description": "Suvoq va bo'yoqdan oldin yuzani mustahkamlovchi astar.",
                    "price": 55000.00,
                    "unit": units["banka"]
                }
            ]
        }
    ]

    total_products = 0
    for cat_data in categories_data:
        category, _ = Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={
                "icon": cat_data["icon"],
                "order": cat_data["order"]
            }
        )
        for prod_data in cat_data["products"]:
            Product.objects.get_or_create(
                name=prod_data["name"],
                category=category,
                defaults={
                    "description": prod_data["description"],
                    "price": prod_data["price"],
                    "unit": prod_data["unit"],
                    "is_active": True
                }
            )
            total_products += 1

    print(f"Muvaffaqiyatli yakunlandi! {len(categories_data)} ta kategoriya va {total_products} ta mahsulot bazaga qo'shildi.")


if __name__ == "__main__":
    populate()
