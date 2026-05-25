from app.repositories.ops_repository import get_active_cities_count

print("Testing active cities count...")
count = get_active_cities_count()
print("ACTIVE CITIES:", count)