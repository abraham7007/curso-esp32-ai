// Mide cuánto del área útil ocupa el CONTENIDO REAL (la tinta) de cada lámina.
// Uso (desde mi-presentacion/): node .ocup.mjs <carpeta-capturas|-> [ancho alto] [archivo...]
//
// Se miden hojas visibles: texto, canvas, svg, img, elementos wokwi-*, botones,
// y cajas con fondo o borde propio. Un contenedor estirado y vacío NO cuenta:
// la primera versión medía cajas y daba 100 % a láminas con media pantalla vacía.

import { readdirSync } from "node:fs";
import { chromium } from "playwright";

const [, , out, w = "1920", h = "1080", ...only] = process.argv;
const CLASE = process.env.CLASE || "clase-01";
const dir = `src/slides/${CLASE}`;
const files = only.length
	? only
	: readdirSync(dir)
			.filter((f) => f.endsWith(".html"))
			.sort();
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: +w, height: +h } });
const errs = [];
p.on("pageerror", (e) => errs.push(String(e)));

for (const f of files) {
	errs.length = 0;
	await p.goto(`http://localhost:5180/src/slides/${CLASE}/${f}#fin`, {
		waitUntil: "networkidle",
	});
	await p.waitForTimeout(900);
	const r = await p.evaluate(() => {
		const slide = document.querySelector(".slide");
		const sr = slide.getBoundingClientRect();
		const cs = getComputedStyle(slide);
		const area = {
			top: sr.top + Number.parseFloat(cs.paddingTop),
			bottom: sr.bottom - Number.parseFloat(cs.paddingBottom),
			left: sr.left + Number.parseFloat(cs.paddingLeft),
			right: sr.right - Number.parseFloat(cs.paddingRight),
		};
		const c = document.querySelector(".slide__content");
		let t = 1e9;
		let bo = -1e9;
		let l = 1e9;
		let ri = -1e9;
		let big = 0;
		let _tintaTotal = 0;
		const add = (rc) => {
			if (rc.width < 2 || rc.height < 2) return;
			t = Math.min(t, rc.top);
			bo = Math.max(bo, rc.bottom);
			l = Math.min(l, rc.left);
			ri = Math.max(ri, rc.right);
		};
		const visible = (el) => {
			const st = getComputedStyle(el);
			return (
				st.display !== "none" &&
				st.visibility !== "hidden" &&
				Number.parseFloat(st.opacity) > 0.05
			);
		};
		const conTinta = (el) => {
			const st = getComputedStyle(el);
			const fondo = !/rgba\(0, 0, 0, 0\)|transparent/.test(st.backgroundColor);
			const borde =
				Number.parseFloat(st.borderTopWidth) > 0 ||
				Number.parseFloat(st.borderLeftWidth) > 0;
			return fondo || borde;
		};
		const walk = (el) => {
			if (!visible(el)) return;
			if (el.closest(".notas, .detalle")) return;
			const tag = el.tagName.toLowerCase();
			if (
				["canvas", "svg", "img", "button", "input"].includes(tag) ||
				tag.startsWith("wokwi-")
			) {
				const rc = el.getBoundingClientRect();
				add(rc);
				if (
					tag !== "button" &&
					tag !== "input" &&
					!el.classList.contains("icon")
				) {
					big = Math.max(big, rc.width * rc.height);
				}
				return;
			}
			if (el !== c && conTinta(el)) {
				const rc = el.getBoundingClientRect();
				add(rc);
				if (el.children.length > 1) big = Math.max(big, rc.width * rc.height);
			}
			for (const n of el.childNodes) {
				if (n.nodeType === 3 && n.textContent.trim()) {
					const range = document.createRange();
					range.selectNodeContents(n);
					for (const rc of range.getClientRects()) {
						add(rc);
						_tintaTotal += rc.width * rc.height;
					}
				}
			}
			for (const ch of el.children) walk(ch);
		};
		walk(c);
		const H = area.bottom - area.top;
		const W = area.right - area.left;
		return {
			vert: (bo - t) / H,
			horiz: (ri - l) / W,
			topGap: (t - area.top) / H,
			botGap: (area.bottom - bo) / H,
			visual: big / (H * W),
			ov: c.scrollHeight - c.clientHeight,
		};
	});
	const mal =
		r.vert < 0.88 ||
		r.topGap > 0.06 ||
		r.botGap > 0.06 ||
		r.ov > 0 ||
		errs.length;
	const pct = (x) => `${(x * 100).toFixed(0)}%`;
	console.log(
		f.padEnd(38),
		`alto ${pct(r.vert)}  ancho ${pct(r.horiz)}  hueco-arriba ${pct(r.topGap)}  hueco-abajo ${pct(r.botGap)}  visual ${pct(r.visual)}  ov ${r.ov}`,
		errs.length ? `ERR ${errs[0]}` : "",
		mal ? "  <<< REVISAR" : "",
	);
	if (out !== "-")
		await p.screenshot({ path: `${out}/${w}_${f.replace(".html", "")}.png` });
}
await b.close();
