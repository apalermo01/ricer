from ricer.utils.theme_data import ThemeData 
import json

if __name__ == '__main__':
    schema = ThemeData.model_json_schema()
    with open("ricer_schema.json", "w") as f:
        json.dump(schema, f, indent=2)
