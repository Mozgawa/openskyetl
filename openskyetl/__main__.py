"""Entry point when invoked with python -m openskyetl."""

if __name__ == "__main__":
    import sys

    from openskyetl.pipeline import main

    if sys.argv[0].endswith("__main__.py"):
        sys.argv[0] = "python -m openskyetl"
    main()
