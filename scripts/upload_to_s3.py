import argparse
import os
from pathlib import Path

import boto3
from botocore.exceptions import NoCredentialsError


def parse_args():
    parser = argparse.ArgumentParser(description="Upload a file to S3")
    parser.add_argument("--bucket", required=True, help="S3 bucket name")
    parser.add_argument("--key", default="sample_data.csv", help="S3 object key")
    parser.add_argument(
        "--file",
        default=None,
        help="Path to local file (default: data/sample_data.csv)",
    )
    parser.add_argument("--region", default=None, help="AWS region (optional)")
    parser.add_argument(
        "--profile",
        default=None,
        help="AWS profile name from ~/.aws/credentials (optional)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    default_file = Path(__file__).resolve().parent.parent / "data" / "sample_data.csv"
    file_path = Path(args.file) if args.file else default_file

    if not file_path.is_file():
        raise SystemExit(f"File not found: {file_path}")

    session = boto3.Session(region_name=args.region, profile_name=args.profile)
    s3 = session.client("s3")

    try:
        s3.upload_file(str(file_path), args.bucket, args.key)
    except NoCredentialsError:
        raise SystemExit(
            "AWS credentials not found. Run `aws configure` or set "
            "AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY (and AWS_REGION) first."
        )

    print(f"Uploaded {file_path} to s3://{args.bucket}/{args.key}")


if __name__ == "__main__":
    main()
