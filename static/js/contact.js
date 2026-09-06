/* ==========================================================
   Section Contact
   Pengiriman ke endpoint Django plus animasi Anime.js v4

   Listener submit dipasang lebih dulu, baru Anime.js dimuat
   lewat dynamic import. Dengan urutan ini form tidak pernah
   berpindah halaman meskipun CDN animasi gagal dimuat.
   ========================================================== */

const $form = document.querySelector('#contact-form');
const $status = document.querySelector('#contact-status');
const $submit = document.querySelector('.contact-submit');
const $submitIcon = document.querySelector('.contact-submit-icon');
const $modal = document.querySelector('#contact-modal');
const $modalTitle = document.querySelector('#contact-modal-title');
const $modalText = document.querySelector('#contact-modal-text');

const $reveal = [...document.querySelectorAll('.contact [data-reveal]')];
const $icons = [...document.querySelectorAll('.contact-icon')];
const $fields = [...document.querySelectorAll('.contact-card .field')];
const $inputs = [...document.querySelectorAll('.contact-card input, .contact-card textarea')];

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

let anime = null;

if ($form) {
    $form.addEventListener('submit', onSubmit);
    pasangPenutupModal();

    import('https://cdn.jsdelivr.net/npm/animejs/+esm')
        .then((modul) => {
            anime = modul;
            if (!reduceMotion) pasangAnimasi();
        })
        .catch(() => {
            console.warn('Anime.js gagal dimuat. Form tetap berfungsi tanpa animasi.');
        });
}

/* ---------------------------------------------
   Animasi yang sifatnya hiasan
   --------------------------------------------- */
function pasangAnimasi() {
    const { animate, createTimeline, stagger, utils, onScroll } = anime;

    utils.set($reveal, { opacity: 0, y: 28 });
    utils.set($icons, { opacity: 0, scale: 0.6 });

    createTimeline({
        defaults: { duration: 700, ease: 'outQuad' },
        autoplay: onScroll({ target: '.contact', enter: 'bottom-=100 top' }),
    })
    .add($reveal, { opacity: 1, y: 0, delay: stagger(120) })
    .add($icons, { opacity: 1, scale: 1, duration: 500, ease: 'outBack', delay: stagger(60) }, '-=300');

    $inputs.forEach(($input) => {
        const $field = $input.closest('.field');
        const $line = $field.querySelector('.field-line');
        const $label = $field.querySelector('label');

        $input.addEventListener('focus', () => {
            animate($line, { scaleX: [0, 1], duration: 420, ease: 'outExpo' });
            animate($label, { x: 4, duration: 300, ease: 'outQuad' });
        });

        $input.addEventListener('blur', () => {
            animate($line, { scaleX: 0, duration: 300, ease: 'outQuad' });
            animate($label, { x: 0, duration: 300, ease: 'outQuad' });
        });
    });

    $icons.forEach(($icon) => {
        const masuk = () => animate($icon, { y: -6, scale: 1.08, duration: 450, ease: 'outBack' });
        const keluar = () => animate($icon, { y: 0, scale: 1, duration: 350, ease: 'outQuad' });

        $icon.addEventListener('mouseenter', masuk);
        $icon.addEventListener('mouseleave', keluar);
        $icon.addEventListener('focus', masuk);
        $icon.addEventListener('blur', keluar);
    });
}

/* ---------------------------------------------
   Proses kirim
   --------------------------------------------- */
async function onSubmit(event) {
    event.preventDefault();

    /* Validasi cepat di sisi browser. Server tetap memvalidasi ulang. */
    const $invalid = $fields.find(($field) => {
        const $control = $field.querySelector('input, textarea');
        return $control && !$control.checkValidity();
    });

    if ($invalid) {
        const $control = $invalid.querySelector('input, textarea');
        tulisStatus('Please complete this field first.');
        goyang($invalid);
        $control.focus();
        return;
    }

    $submit.disabled = true;
    tulisStatus('Sending...');

    const hasil = await kirimKeServer();

    $submit.disabled = false;

    if (hasil.ok) {
        tulisStatus('');
        $form.reset();
        $submitIcon.textContent = 'check';
        setTimeout(() => { $submitIcon.textContent = 'send'; }, 2500);
        bukaModal(
            'Message sent',
            'Thanks for reaching out. I will get back to you as soon as I can.'
        );
        return;
    }

    /* Kalau server menolak karena isian bermasalah, tandai fieldnya */
    const namaField = Object.keys(hasil.errors || {})[0];

    if (namaField) {
        const $control = $form.querySelector(`[name="${namaField}"]`);
        const pesan = hasil.errors[namaField][0].message;

        tulisStatus(pesan);

        if ($control) {
            goyang($control.closest('.field'));
            $control.focus();
        }
        return;
    }

    tulisStatus('');
    bukaModal(
        'Message not sent',
        'Something went wrong on the way. Please try again or email me directly.'
    );
}

/* FormData sudah membawa csrfmiddlewaretoken dari tag {% csrf_token %},
   jadi Django menerima permintaan ini tanpa konfigurasi tambahan. */
async function kirimKeServer() {
    try {
        const response = await fetch($form.action, {
            method: 'POST',
            body: new FormData($form),
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
        });

        const data = await response.json().catch(() => ({}));

        return { ok: response.ok && data.ok === true, errors: data.errors };
    } catch (error) {
        console.error(error);
        return { ok: false, errors: null };
    }
}

function goyang($el) {
    if (!$el || !anime || reduceMotion) return;
    anime.animate($el, { x: [0, -10, 10, -7, 7, 0], duration: 480, ease: 'inOutQuad' });
}

function tulisStatus(teks) {
    if (!$status) return;
    $status.textContent = teks;
    $status.style.opacity = teks ? '1' : '0';
}

/* ---------------------------------------------
   Modal konfirmasi
   --------------------------------------------- */
function bukaModal(judul, pesan) {
    if (!$modal) return;

    $modalTitle.textContent = judul;
    $modalText.textContent = pesan;
    $modal.hidden = false;
    document.body.style.overflow = 'hidden';
    $modal.querySelector('.contact-modal-close').focus();

    if (!anime || reduceMotion) return;

    const { animate } = anime;

    animate($modal.querySelector('.contact-modal-backdrop'), {
        opacity: [0, 1],
        duration: 260,
        ease: 'outQuad',
    });
    animate($modal.querySelector('.contact-modal-box'), {
        opacity: [0, 1],
        scale: [0.85, 1],
        y: [20, 0],
        duration: 520,
        ease: 'outBack',
    });
    animate($modal.querySelector('.contact-modal-icon'), {
        scale: [0, 1],
        rotate: [-40, 0],
        duration: 620,
        delay: 120,
        ease: 'outBack',
    });
}

function tutupModal() {
    if (!$modal || $modal.hidden) return;

    document.body.style.overflow = '';

    if (!anime || reduceMotion) {
        $modal.hidden = true;
        return;
    }

    anime.animate($modal.querySelector('.contact-modal-box'), {
        opacity: 0,
        scale: 0.92,
        duration: 220,
        ease: 'inQuad',
    });
    anime.animate($modal.querySelector('.contact-modal-backdrop'), {
        opacity: 0,
        duration: 260,
        ease: 'inQuad',
        onComplete: () => { $modal.hidden = true; },
    });
}

function pasangPenutupModal() {
    if (!$modal) return;

    $modal.querySelectorAll('[data-close]').forEach(($el) => {
        $el.addEventListener('click', tutupModal);
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') tutupModal();
    });
}