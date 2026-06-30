import siteContent from "../content/site-content.md?raw";
import { parseSiteContent } from "./contentParser.js";

export const { siteMeta, products } = parseSiteContent(siteContent);
