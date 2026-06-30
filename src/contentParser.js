const PRODUCT_ARRAY_FIELDS = new Set(["highlights", "useCases", "materials"]);

function parseFieldLines(lines) {
  const data = {};
  let currentArrayKey = "";

  for (const rawLine of lines) {
    const line = rawLine.trimEnd();
    if (!line.trim()) {
      continue;
    }

    const fieldMatch = line.match(/^- ([A-Za-z][A-Za-z0-9]*):\s*(.*)$/);
    if (fieldMatch) {
      const [, key, value] = fieldMatch;
      currentArrayKey = "";
      if (PRODUCT_ARRAY_FIELDS.has(key) && value === "") {
        data[key] = [];
        currentArrayKey = key;
        continue;
      }
      data[key] = value;
      continue;
    }

    const itemMatch = line.match(/^  -\s+(.*)$/);
    if (itemMatch && currentArrayKey) {
      data[currentArrayKey].push(itemMatch[1]);
    }
  }

  return data;
}

function getSection(markdown, title) {
  const lines = markdown.split("\n");
  const startIndex = lines.findIndex((line) => line.trim() === `## ${title}`);
  if (startIndex === -1) {
    return "";
  }

  const rest = lines.slice(startIndex + 1);
  const endIndex = rest.findIndex((line) => line.startsWith("## "));
  return (endIndex === -1 ? rest : rest.slice(0, endIndex)).join("\n").trim();
}

function parseProducts(markdown) {
  const productsSection = getSection(markdown, "工具目录");
  return productsSection
    .split(/^### /m)
    .slice(1)
    .map((block, index) => {
      const [heading, ...rest] = block.split("\n");
      const fields = parseFieldLines(rest);
      return {
        ...fields,
        name: fields.name || heading.trim(),
        index: String(index + 1).padStart(2, "0"),
        highlights: fields.highlights || [],
        useCases: fields.useCases || [],
        materials: fields.materials || [],
      };
    });
}

export function parseSiteContent(markdown) {
  const siteMeta = parseFieldLines(getSection(markdown, "站点信息").split("\n"));
  return {
    siteMeta,
    products: parseProducts(markdown),
  };
}
