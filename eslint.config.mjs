import { defineConfig } from "eslint/config";
import globals from "globals";
import js from "@eslint/js";

export default defineConfig([
  js.configs.all,
  {
    files: ["**/*.js"],
    languageOptions: { globals: globals.browser },
    rules: {
      "max-statements": "off",
      "no-magic-numbers": "off",
      "no-use-before-define": "off",
      "no-ternary": "off",
      "one-var": "off",
    },
  }
]);
