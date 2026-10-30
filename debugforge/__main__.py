import argparse

from .orchestrator import debug_repository


def main():
    parser = argparse.ArgumentParser(
        description="DebugForge - Autonomous debugging and repair agent"
    )

    parser.add_argument(
        "--repo",
        required=True,
        help="Path to the repository to debug"
    )

    parser.add_argument(
        "--test",
        required=True,
        help="Test command to run"
    )

    args = parser.parse_args()

    print()
    print("DebugForge")
    print("----------")
    print()
    print(f"Repository: {args.repo}")
    print(f"Test command: {args.test}")
    print()
    print("Running debugging agent...")
    print()

    try:
        result = debug_repository(
            repo_path=args.repo,
            test_command=args.test
        )

        print(f"Status: {result['status']}")
        print()

        evidence = result.get("evidence", {})

        if evidence:
            print("Failure Analysis:")
            print(f"  Test file: {evidence.get('test_file')}")
            print(f"  Test name: {evidence.get('test_name')}")
            print(f"  Error: {evidence.get('error')}")

            if evidence.get("source_file"):
                print(f"  Source file: {evidence.get('source_file')}")

            if evidence.get("source_function"):
                print(f"  Source function: {evidence.get('source_function')}")

            print()

        repair = result.get("repair")

        if repair:
            print("Repair:")
            print(f"  File: {repair.file_path}")
            print(f"  Diagnosis: {repair.diagnosis}")
            print()

        repair_result = result.get("repair_result")

        if repair_result:
            print(f"Verification: {repair_result['status']}")

            if repair_result.get("diff"):
                print()
                print("Patch:")
                print(repair_result["diff"])

        print()

        if result["status"] == "VERIFIED":
            print("✓ DebugForge successfully repaired the bug.")
        elif result["status"] == "PASSED":
            print("✓ Tests already pass. No repair was needed.")
        else:
            print("✗ DebugForge could not verify a successful repair.")

    except Exception as error:
        print(f"Error: {error}")
        raise


if __name__ == "__main__":
    main()