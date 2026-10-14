/* Lienzo adaptable para las simulaciones de las láminas en modo ponencia.

   El canvas ocupa la caja que le da el CSS (.lienzo-caja) y aquí se ajusta su
   resolución interna a ese tamaño real por devicePixelRatio, de modo que la
   simulación llena el escenario sin deformarse ni verse borrosa. El dibujo
   trabaja en píxeles CSS: dibujar(ctx, ancho, alto).

   Redibuja al cambiar de tamaño, al conmutar el tema (data-theme o la
   preferencia del sistema) y cuando terminan de cargar las fuentes.

     import { lienzoAdaptable, token } from "../../js/lienzo.js";
     const lienzo = lienzoAdaptable(canvas, (ctx, w, h) => { ... });
     lienzo.redibujar();   // tras cambiar el estado de la simulación */

export const token = (nombre) =>
	getComputedStyle(document.documentElement).getPropertyValue(nombre).trim();

export function lienzoAdaptable(canvas, dibujar) {
	const ctx = canvas.getContext("2d");
	let ancho = 0;
	let alto = 0;

	const redibujar = () => {
		if (!ancho || !alto) return;
		const dpr = window.devicePixelRatio || 1;
		ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
		ctx.clearRect(0, 0, ancho, alto);
		dibujar(ctx, ancho, alto);
	};

	const medir = () => {
		const r = canvas.getBoundingClientRect();
		const dpr = window.devicePixelRatio || 1;
		ancho = r.width;
		alto = r.height;
		canvas.width = Math.max(1, Math.round(ancho * dpr));
		canvas.height = Math.max(1, Math.round(alto * dpr));
		redibujar();
	};

	new ResizeObserver(medir).observe(canvas);
	new MutationObserver(redibujar).observe(document.documentElement, {
		attributes: true,
		attributeFilter: ["data-theme"],
	});
	window
		.matchMedia("(prefers-color-scheme: dark)")
		.addEventListener("change", redibujar);
	document.fonts?.ready.then(redibujar);
	medir();

	return {
		redibujar,
		get ancho() {
			return ancho;
		},
		get alto() {
			return alto;
		},
	};
}
