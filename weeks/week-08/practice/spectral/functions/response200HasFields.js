export default function response200HasFields(response) {
  const content = response?.content;
  const mediaTypes = content ? Object.values(content) : [];

  const hasFields = (schema) => {
    if (!schema || typeof schema !== "object") return false;

    if (schema.properties && Object.keys(schema.properties).length > 0) {
      return true;
    }

    if (schema.type === "array" && hasFields(schema.items)) {
      return true;
    }

    return [schema.allOf, schema.oneOf, schema.anyOf]
      .filter(Array.isArray)
      .some((schemas) => schemas.some(hasFields));
  };

  if (mediaTypes.length > 0 && mediaTypes.every((mediaType) => hasFields(mediaType.schema))) {
    return;
  }

  return [
    {
      message: "200 response must have more than 0 fields in its schema.",
    },
  ];
}
