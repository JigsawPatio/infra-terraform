import os
import json
from infra_terraform import TerraformRunner

def main():
    with open('terraform.tf.json', 'r') as f:
        terraform_config = json.load(f)

    runner = TerraformRunner(
        terraform_config,
        workspace_name='my_workspace',
        working_directory='/path/to/working/directory',
        backend_config={
            'bucket': 'my-bucket',
            'key': 'my-key',
            'region': 'my-region',
        },
    )

    runner.apply()

if __name__ == '__main__':
    main()