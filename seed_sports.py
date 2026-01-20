from apps.gestion_operativa.models import Deporte, DeportesChoices


def seed_sports():
    print("Seeding sports...")
    count = 0
    for code, label in DeportesChoices.choices:
        obj, created = Deporte.objects.get_or_create(
            codigo=code, defaults={"nombre": label}
        )
        if created:
            print(f"Created sport: {label} ({code})")
            count += 1
        else:
            # Update name if changed (optional but good for consistency)
            if obj.nombre != label:
                obj.nombre = label
                obj.save()
                print(f"Updated sport: {label} ({code})")

    print(f"Seeding complete. {count} new sports created.")
    print(f"Total sports: {Deporte.objects.count()}")


if __name__ == "__main__":
    seed_sports()
