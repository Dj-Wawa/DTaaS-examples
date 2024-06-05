import sys


def read_template(template_path):
    with open(template_path, 'r') as file:
        return file.read()


def write_config(output_path, content):
    with open(output_path, 'w') as file:
        file.write(content)


def create_configs(template_path, num_configs):
    template_content = read_template(template_path)

    for n in range(1, num_configs + 1):
        config_content = template_content.replace('<ID>', str(n))
        output_path = f'../configs/{n}'
        write_config(output_path, config_content)
        print(f'Created: {output_path}')


def create_specs(template_path, num_configs):
    template_content = read_template(template_path)

    for n in range(1, num_configs + 1):
        config_content = template_content.replace('<ID>', str(n))
        output_path = f'../../../tools/tessla-telegraf-connector/specification-{n}.tessla'
        write_config(output_path, config_content)
        print(f'Created: {output_path}')


if __name__ == "__main__":
    template_path = '../config.template'  # Path to the template configuration file
    num_configs = int(sys.argv[1])

create_configs(template_path, num_configs)
create_specs('../../../tools/tessla-telegraf-connector/specification.template', num_configs)
