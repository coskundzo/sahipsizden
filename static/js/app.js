let data = {}; // Will be loaded from API

const category = document.getElementById("category");
const brand = document.getElementById("brand");
const series = document.getElementById("series");
const engine = document.getElementById("engine"); // motor tipi
const packageEl = document.getElementById("package"); // paket
const year = document.getElementById("year");
const analyzeBtn = document.getElementById("analyzeBtn");

const breadcrumb = document.getElementById("breadcrumb");

function reset(select, message = "Seç") {
    select.innerHTML = `<option value=''>${message}</option>`;
    select.disabled = true;
}

function enable(select, message = "Seçin") {
    if (select.options.length > 1) {
        select.disabled = false;
    }
}

// Generate car image URL based on brand and model
function getCarImageUrl(brand, series) {
    // Map of brand-specific Unsplash photo IDs or searches
    const brandImages = {
        'BMW': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&h=600&fit=crop',
        'Mercedes-Benz': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&h=600&fit=crop',
        'Audi': 'https://images.unsplash.com/photo-1610768764270-790fbec18178?w=800&h=600&fit=crop',
        'Volkswagen': 'https://images.unsplash.com/photo-1622353219448-46a2c8c0c58f?w=800&h=600&fit=crop',
        'Toyota': 'https://images.unsplash.com/photo-1629897048514-3dd7414fe72a?w=800&h=600&fit=crop',
        'Renault': 'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&h=600&fit=crop',
        'Ford': 'https://images.unsplash.com/photo-1612825173281-9a193378527e?w=800&h=600&fit=crop',
        'Peugeot': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&h=600&fit=crop',
        'Fiat': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800&h=600&fit=crop',
        'Opel': 'https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=800&h=600&fit=crop',
        'Alfa Romeo': 'https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=800&h=600&fit=crop'
    };
    
    // Return brand-specific image or fallback to generic car
    return brandImages[brand] || 'https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&h=600&fit=crop';
}

// KATEGORİLER
async function loadCategories() {
    // Fetch data from API
    try {
        const response = await fetch("/api/cars");
        data = await response.json();
    } catch (error) {
        console.error("Failed to load cars data:", error);
        return;
    }
    
    reset(category);
    for (let c in data) {
        category.innerHTML += `<option value="${c}">${c}</option>`;
    }
    // Set default image and title
    document.getElementById("carImage").src = "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&auto=format&fit=crop&q=80";
    document.getElementById("carTitle").innerText = "Araç Seçiniz";
    document.getElementById("carBadge").style.display = "none";
    
    // Enable category selection
    enable(category);
}

// Update dropdowns for new structure
category.onchange = () => {
    reset(brand, "Marka seçin");
    reset(series, "Önce marka seçin");
    reset(engine, "Önce model seçin");
    reset(packageEl, "Önce motor seçin");
    reset(year, "Önce paket seçin");
    analyzeBtn.disabled = true;
    
    let b = data[category.value] || {};
    for (let key in b) {
        brand.innerHTML += `<option value="${key}">${key}</option>`;
    }
    
    if (!category.value) {
        document.getElementById("carImage").src = "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&auto=format&fit=crop&q=80";
        document.getElementById("carTitle").innerText = "Araç Seçiniz";
        document.getElementById("carBadge").style.display = "none";
    } else {
        enable(brand);
    }
    updateBreadcrumb();
};

brand.onchange = () => {
    reset(series, "Model seçin");
    reset(engine, "Önce model seçin");
    reset(packageEl, "Önce motor seçin");
    reset(year, "Önce paket seçin");
    analyzeBtn.disabled = true;
    
    let s = data[category.value]?.[brand.value] || {};
    for (let key in s) {
        series.innerHTML += `<option value="${key}">${key}</option>`;
    }
    
    if (!brand.value) {
        document.getElementById("carImage").src = "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&auto=format&fit=crop&q=80";
        document.getElementById("carTitle").innerText = "Araç Seçiniz";
        document.getElementById("carBadge").style.display = "none";
    } else {
        enable(series);
    }
    updateBreadcrumb();
};

series.onchange = () => {
    reset(engine, "Motor tipi seçin");
    reset(packageEl, "Önce motor seçin");
    reset(year, "Önce paket seçin");
    analyzeBtn.disabled = true;
    
    let e = data[category.value]?.[brand.value]?.[series.value] || {};
    for (let key in e) {
        engine.innerHTML += `<option value="${key}">${key}</option>`;
    }
    
    if (!series.value) {
        document.getElementById("carImage").src = "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&auto=format&fit=crop&q=80";
        document.getElementById("carTitle").innerText = "Araç Seçiniz";
        document.getElementById("carBadge").style.display = "none";
    } else {
        enable(engine);
    }
    updateBreadcrumb();
};

engine.onchange = () => {
    reset(packageEl, "Paket seçin");
    reset(year, "Önce paket seçin");
    analyzeBtn.disabled = true;
    
    let p = data[category.value]?.[brand.value]?.[series.value]?.[engine.value] || {};
    for (let key in p) {
        packageEl.innerHTML += `<option value="${key}">${key}</option>`;
    }
    
    if (!engine.value) {
        document.getElementById("carImage").src = "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&auto=format&fit=crop&q=80";
        document.getElementById("carTitle").innerText = "Araç Seçiniz";
        document.getElementById("carBadge").style.display = "none";
    } else {
        enable(packageEl);
    }
    updateBreadcrumb();
};

packageEl.onchange = () => {
    reset(year, "Yıl seçin");
    analyzeBtn.disabled = true;
    
    let y = data[category.value]?.[brand.value]?.[series.value]?.[engine.value]?.[packageEl.value] || {};
    for (let key in y) {
        year.innerHTML += `<option value="${key}">${key}</option>`;
    }
    
    if (!packageEl.value) {
        document.getElementById("carImage").src = "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&auto=format&fit=crop&q=80";
        document.getElementById("carTitle").innerText = "Araç Seçiniz";
        document.getElementById("carBadge").style.display = "none";
    } else {
        enable(year);
    }
    updateBreadcrumb();
};

year.onchange = () => {
    const car = data[category.value]?.[brand.value]?.[series.value]?.[engine.value]?.[packageEl.value]?.[year.value];
    
    if (year.value) {
        // Get brand-specific car image
        const imageUrl = getCarImageUrl(brand.value, series.value);
        
        document.getElementById("carImage").src = imageUrl;
        document.getElementById("carTitle").innerText = `${category.value} - ${brand.value} ${series.value} ${engine.value} ${packageEl.value} (${year.value})`;
        document.getElementById("carBadge").style.display = "inline-block";
        analyzeBtn.disabled = false;
    } else {
        document.getElementById("carImage").src = "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&auto=format&fit=crop&q=80";
        document.getElementById("carTitle").innerText = "Araç Seçiniz";
        document.getElementById("carBadge").style.display = "none";
        analyzeBtn.disabled = true;
    }
    
    updateBreadcrumb();
};


// BREADCRUMB UPDATE
function updateBreadcrumb() {
    const parts = [];
    if (category.value) parts.push(category.value);
    if (brand.value) parts.push(brand.value);
    if (series.value) parts.push(series.value);
    if (engine.value) parts.push(engine.value);
    if (packageEl.value) parts.push(packageEl.value);
    if (year.value) parts.push(year.value);
    
    breadcrumb.innerText = parts.length > 0 ? parts.join(" › ") : "Araç seçimi yapın";
}

// ANALİZ
async function analyze() {
    if (!year.value) {
        alert("Lütfen tüm alanları doldurun!");
        return;
    }
    
    const resultContainer = document.getElementById("resultContainer");
    const btnText = document.getElementById("btnText");
    
    // Loading state
    analyzeBtn.disabled = true;
    btnText.innerHTML = '<span class="loading"></span> Analiz ediliyor...';
    resultContainer.innerHTML = `
        <div class="analyzing">
            <div class="loading"></div>
            <span>AI analiz yapıyor, lütfen bekleyin...</span>
        </div>
    `;

    try {
        const res = await fetch("/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                brand: brand.value,
                series: series.value,
                engine: engine.value,
                package: packageEl.value,
                year: year.value
            })
        });

        const json = await res.json();
        
        if (json.error) {
            resultContainer.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">⚠️</div>
                    <h4>Hata Oluştu</h4>
                    <p>${json.error}</p>
                </div>
            `;
        } else {
            resultContainer.innerHTML = `<pre id="result">${json.result}</pre>`;
        }
    } catch (error) {
        resultContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">❌</div>
                <h4>Bağlantı Hatası</h4>
                <p>Sunucuya bağlanılamadı. Lütfen tekrar deneyin.</p>
            </div>
        `;
    } finally {
        analyzeBtn.disabled = false;
        btnText.innerHTML = '🔍 Analiz Yap';
    }
}

// Ensure loadCategories runs after DOM is ready
document.addEventListener("DOMContentLoaded", function() {
    loadCategories();
});