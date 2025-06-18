module.exports = {
  content: ["./templates/**/*.html", "./**/templates/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light", "dark", "cupcake", "synthwave", "pastel", "dracula", "business"],
  },
};
