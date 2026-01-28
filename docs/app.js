// ===========================
// State Management
// ===========================
let allInternships = [];
let filteredInternships = [];

// ===========================
// DOM Elements
// ===========================
const elements = {
    searchInput: document.getElementById('searchInput'),
    clearBtn: document.getElementById('clearBtn'),
    typeFilter: document.getElementById('typeFilter'),
    locationFilter: document.getElementById('locationFilter'),
    sortBy: document.getElementById('sortBy'),
    resetFilters: document.getElementById('resetFilters'),
    internshipsGrid: document.getElementById('internshipsGrid'),
    loadingState: document.getElementById('loadingState'),
    errorState: document.getElementById('errorState'),
    emptyState: document.getElementById('emptyState'),
    resultsInfo: document.getElementById('resultsInfo'),
    resultsCount: document.getElementById('resultsCount'),
    totalCount: document.getElementById('totalCount'),
    lastUpdated: document.getElementById('lastUpdated')
};

// ===========================
// Utility Functions
// ===========================
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function formatStipend(stipend) {
    if (!stipend || (!stipend.min && !stipend.max)) return 'Unpaid';
    
    const currency = stipend.currency || 'INR';
    const symbol = currency === 'INR' ? '₹' : '$';
    
    if (stipend.min && stipend.max && stipend.min !== stipend.max) {
        return `${symbol}${formatNumber(stipend.min)} - ${symbol}${formatNumber(stipend.max)}`;
    }
    
    const amount = stipend.max || stipend.min;
    return `${symbol}${formatNumber(amount)}`;
}

function formatNumber(num) {
    if (num >= 100000) return `${(num / 100000).toFixed(1)}L`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
}

function truncateText(text, maxLength) {
    if (!text || text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// ===========================
// Data Loading
// ===========================
async function loadInternships() {
    try {
        elements.loadingState.style.display = 'block';
        elements.errorState.style.display = 'none';
        elements.emptyState.style.display = 'none';
        
        const response = await fetch('data/internships.json');
        
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        
        const data = await response.json();
        
        allInternships = data.internships || [];
        filteredInternships = [...allInternships];
        
        // Update header stats
        elements.totalCount.textContent = data.totalInternships || 0;
        elements.lastUpdated.textContent = formatDate(data.lastUpdated);
        
        elements.loadingState.style.display = 'none';
        
        applyFilters();
        
    } catch (error) {
        console.error('Error loading internships:', error);
        elements.loadingState.style.display = 'none';
        elements.errorState.style.display = 'block';
    }
}

// ===========================
// Filtering & Sorting
// ===========================
function applyFilters() {
    const searchTerm = elements.searchInput.value.toLowerCase().trim();
    const typeFilter = elements.typeFilter.value;
    const locationFilter = elements.locationFilter.value;
    const sortBy = elements.sortBy.value;
    
    // Filter
    filteredInternships = allInternships.filter(internship => {
        // Search filter
        if (searchTerm) {
            const searchableText = [
                internship.title,
                internship.company,
                internship.location,
                ...(internship.skills || [])
            ].join(' ').toLowerCase();
            
            if (!searchableText.includes(searchTerm)) {
                return false;
            }
        }
        
        // Type filter
        if (typeFilter && internship.type !== typeFilter) {
            return false;
        }
        
        // Location filter
        if (locationFilter === 'wfh' && !internship.workFromHome) {
            return false;
        }
        
        return true;
    });
    
    // Sort
    filteredInternships.sort((a, b) => {
        switch (sortBy) {
            case 'recent':
                return new Date(b.scrapedAt) - new Date(a.scrapedAt);
            
            case 'stipend-high':
                const stipendA = (a.stipend?.max || a.stipend?.min || 0);
                const stipendB = (b.stipend?.max || b.stipend?.min || 0);
                return stipendB - stipendA;
            
            case 'views':
                return (b.views || 0) - (a.views || 0);
            
            case 'registrations':
                return (b.registrations || 0) - (a.registrations || 0);
            
            default:
                return 0;
        }
    });
    
    renderInternships();
}

// ===========================
// Rendering
// ===========================
function renderInternships() {
    elements.internshipsGrid.innerHTML = '';
    
    if (filteredInternships.length === 0) {
        elements.emptyState.style.display = 'block';
        elements.resultsInfo.style.display = 'none';
        return;
    }
    
    elements.emptyState.style.display = 'none';
    elements.resultsInfo.style.display = 'block';
    elements.resultsCount.textContent = filteredInternships.length;
    
    filteredInternships.forEach(internship => {
        const card = createInternshipCard(internship);
        elements.internshipsGrid.appendChild(card);
    });
}

function createInternshipCard(internship) {
    const card = document.createElement('div');
    card.className = 'internship-card';
    card.onclick = () => window.open(internship.url, '_blank');
    
    const logoUrl = internship.logo || 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"%3E%3Crect width="100" height="100" fill="%23e2e8f0"/%3E%3Ctext x="50" y="50" font-family="Arial" font-size="40" fill="%234a5568" text-anchor="middle" dominant-baseline="middle"%3E%3F%3C/text%3E%3C/svg%3E';
    
    card.innerHTML = `
        <div class="card-header">
            <img src="${logoUrl}" alt="${internship.company}" class="company-logo" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' viewBox=\\'0 0 100 100\\'%3E%3Crect width=\\'100\\' height=\\'100\\' fill=\\'%23e2e8f0\\'/%3E%3C/svg%3E'">
            <div class="card-title-section">
                <h3 class="card-title">${internship.title}</h3>
                <p class="card-company">${internship.company}</p>
            </div>
        </div>
        
        <div class="card-badges">
            <span class="badge badge-type">${internship.type || 'Internship'}</span>
            ${internship.workFromHome ? '<span class="badge badge-wfh">🏠 WFH</span>' : ''}
            ${internship.stipend ? `<span class="badge badge-stipend">💰 ${formatStipend(internship.stipend)}</span>` : ''}
        </div>
        
        <div class="card-details">
            ${internship.location ? `
                <div class="detail-item">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                        <circle cx="12" cy="10" r="3"/>
                    </svg>
                    <span>${truncateText(internship.location, 50)}</span>
                </div>
            ` : ''}
            
            ${internship.duration ? `
                <div class="detail-item">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <path d="M12 6v6l4 2"/>
                    </svg>
                    <span>${internship.duration}</span>
                </div>
            ` : ''}
            
            ${internship.deadline ? `
                <div class="detail-item">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                        <path d="M16 2v4M8 2v4M3 10h18"/>
                    </svg>
                    <span><strong>Deadline:</strong> ${formatDate(internship.deadline)}</span>
                </div>
            ` : ''}
        </div>
        
        ${internship.skills && internship.skills.length > 0 ? `
            <div class="skills-list">
                ${internship.skills.slice(0, 5).map(skill => 
                    `<span class="skill-tag">${skill}</span>`
                ).join('')}
                ${internship.skills.length > 5 ? `<span class="skill-tag">+${internship.skills.length - 5} more</span>` : ''}
            </div>
        ` : ''}
        
        <div class="card-footer">
            <div class="card-stats">
                ${internship.views ? `
                    <div class="stat-item">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                            <circle cx="12" cy="12" r="3"/>
                        </svg>
                        ${formatNumber(internship.views)}
                    </div>
                ` : ''}
                ${internship.registrations ? `
                    <div class="stat-item">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                            <circle cx="9" cy="7" r="4"/>
                            <path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>
                        </svg>
                        ${formatNumber(internship.registrations)}
                    </div>
                ` : ''}
            </div>
            <button class="apply-btn" onclick="event.stopPropagation(); window.open('${internship.url}', '_blank');">
                Apply Now →
            </button>
        </div>
    `;
    
    return card;
}

// ===========================
// Event Listeners
// ===========================
function setupEventListeners() {
    // Search
    elements.searchInput.addEventListener('input', (e) => {
        elements.clearBtn.style.display = e.target.value ? 'block' : 'none';
        debounce(applyFilters, 300)();
    });
    
    elements.clearBtn.addEventListener('click', () => {
        elements.searchInput.value = '';
        elements.clearBtn.style.display = 'none';
        applyFilters();
    });
    
    // Filters
    elements.typeFilter.addEventListener('change', applyFilters);
    elements.locationFilter.addEventListener('change', applyFilters);
    elements.sortBy.addEventListener('change', applyFilters);
    
    // Reset
    elements.resetFilters.addEventListener('click', () => {
        elements.searchInput.value = '';
        elements.clearBtn.style.display = 'none';
        elements.typeFilter.value = '';
        elements.locationFilter.value = '';
        elements.sortBy.value = 'recent';
        applyFilters();
    });
}

// ===========================
// Debounce Helper
// ===========================
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ===========================
// Initialize
// ===========================
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadInternships();
});
