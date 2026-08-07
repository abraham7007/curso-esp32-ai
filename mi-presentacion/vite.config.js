import { readdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

const RAIZ = path.dirname(fileURLToPath(import.meta.url));
const SLIDES = path.join(RAIZ, "src", "slides");

/* Vite construye por defecto una sola página: index.html. Cada diapositiva es
   un documento independiente, así que sin declararlas aquí `npm run build`
   producía un dist/ con el índice y ningún enlace funcionando. Se recogen del
   disco en lugar de listarlas a mano para que añadir una diapositiva nueva no
   exija acordarse de tocar este archivo. */
function entradasDeDiapositivas() {
	const entradas = {
		index: path.join(RAIZ, "index.html"),
		// Marco del modo presentación: mantiene viva la pantalla completa
		// mientras las diapositivas se suceden dentro.
		presentar: path.join(RAIZ, "presentar.html"),
	};
	for (const clase of readdirSync(SLIDES)) {
		const dir = path.join(SLIDES, clase);
		for (const archivo of readdirSync(dir)) {
			if (!archivo.endsWith(".html")) continue;
			const nombre = `${clase}/${archivo.replace(/\.html$/, "")}`;
			entradas[nombre] = path.join(dir, archivo);
		}
	}
	return entradas;
}

export default defineConfig({
	plugins: [tailwindcss()],
	build: {
		rollupOptions: {
			input: entradasDeDiapositivas(),
		},
	},
});
