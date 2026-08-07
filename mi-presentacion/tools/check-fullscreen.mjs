/* Comprueba que la pantalla completa sobrevive al avance entre láminas.

   Era el fallo reportado: cada diapositiva es un documento distinto y la API
   de pantalla completa muere con el documento, así que pulsar «siguiente»
   devolvía a modo ventana. Esta prueba avanza varias láminas y verifica que
   el documento contenedor sigue en pantalla completa después de cada salto. */

import { chromium } from "playwright";
import { asegurarServidor } from "./lib/servidor.mjs";

const BASE = "http://localhost:5173";
await asegurarServidor();

const nav = await chromium.launch({ channel: "chrome" });
const pagina = await nav.newPage({ viewport: { width: 1280, height: 800 } });

const enPantallaCompleta = () =>
	pagina.evaluate(() => Boolean(document.fullscreenElement));
const rutaInterior = () =>
	pagina.evaluate(
		() => document.getElementById("marco").contentWindow.location.pathname,
	);

await pagina.goto(
	`${BASE}/presentar.html#/src/slides/clase-01/01-portada.html`,
	{
		waitUntil: "networkidle",
	},
);
await pagina.waitForTimeout(400);

console.log(
	"antes del gesto:",
	await enPantallaCompleta(),
	"|",
	await rutaInterior(),
);

// Primer gesto: debe entrar en pantalla completa.
await pagina.keyboard.press("ArrowRight");
await pagina.waitForTimeout(700);
console.log(
	"tras 1er gesto:",
	await enPantallaCompleta(),
	"|",
	await rutaInterior(),
);

const fallos = [];
for (let i = 2; i <= 6; i++) {
	// Sin tocar el foco a mano: el marco debe devolverlo a la diapositiva por
	// su cuenta, que es lo que hace que las flechas funcionen de verdad.
	await pagina.keyboard.press("ArrowRight");
	await pagina.waitForTimeout(600);
	const fs = await enPantallaCompleta();
	const ruta = await rutaInterior();
	console.log(`salto ${i}: pantalla completa = ${fs} | ${ruta}`);
	if (!fs) fallos.push(`salto ${i}`);
}

await nav.close();

if (fallos.length) {
	console.log(`\n✗ se salió de pantalla completa en: ${fallos.join(", ")}`);
	process.exitCode = 1;
} else {
	console.log("\n✓ la pantalla completa se mantuvo en todos los saltos");
}

/* --------------------------------------------------------------------------
   Segundo escenario: el recorrido real del usuario. Se abre una diapositiva
   suelta, se pulsa su botón de pantalla completa y se comprueba que acaba en
   el modo presentación, que entra a pantalla completa y que avanzar con el
   ratón la conserva.
   -------------------------------------------------------------------------- */

const nav2 = await chromium.launch({ channel: "chrome" });
const p2 = await nav2.newPage({ viewport: { width: 1280, height: 800 } });

await p2.goto(`${BASE}/src/slides/clase-01/10-conversion-adc.html`, {
	waitUntil: "networkidle",
});
await p2.click('.deck-controls__btn[aria-label="Pantalla completa"]');
await p2.waitForURL(/presentar\.html/, { timeout: 5000 });
await p2.waitForTimeout(600);

const dentro = () =>
	p2.evaluate(
		() => document.getElementById("marco").contentWindow.location.pathname,
	);
const fs2 = () => p2.evaluate(() => Boolean(document.fullscreenElement));

console.log("\n--- desde el botón de una lámina suelta ---");
console.log(
	"marco cargado con:",
	await dentro(),
	"| pantalla completa:",
	await fs2(),
);

// Avanzar con el ratón, pulsando el enlace «siguiente» dentro del marco.
const errores = [];
for (let i = 1; i <= 3; i++) {
	const marco = p2.frames()[1];
	await marco.click(".slide-nav a.slide-nav__link:last-of-type");
	await p2.waitForTimeout(700);
	const ok = await fs2();
	console.log(`clic ${i}: pantalla completa = ${ok} | ${await dentro()}`);
	if (!ok) errores.push(`clic ${i}`);
}

await nav2.close();

if (errores.length) {
	console.log(`\n✗ se salió de pantalla completa en: ${errores.join(", ")}`);
	process.exitCode = 1;
} else {
	console.log("✓ el botón lleva al modo presentación y el ratón lo conserva");
}
