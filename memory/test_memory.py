from .spine import MemorySpine

def main() -> None:
    spine = MemorySpine()

    print("Writing sample event…")
    spine.write("note", {"text": "Hello from C3 memory v1"})

    print("Reading all events:")
    for e in spine.read_all():
        print(e)


if __name__ == "__main__":
    main()
