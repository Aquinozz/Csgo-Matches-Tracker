// Pesquisa de times
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchTeamInput');
    const searchBtn = document.getElementById('searchTeamBtn');
    const searchResults = document.getElementById('searchResults');

    if (searchInput && searchBtn) {
        searchBtn.addEventListener('click', buscarTime);
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') buscarTime();
        });

        async function buscarTime() {
            const nometime = searchInput.value.trim();
            if (!nometime) {
                searchResults.innerHTML = '<p class="no-results">Digite o nome de um time</p>';
                return;
            }

            try {
                searchResults.innerHTML = '<p class="loading">Buscando...</p>';
                const response = await fetch(`/api/buscar-times?nome=${encodeURIComponent(nometime)}`);
                const data = await response.json();

                if (data.times && data.times.length > 0) {
                    let html = '<div class="teams-grid">';
                    data.times.forEach(time => {
                        const pais = time.country || time.location || 'País desconhecido';
                        html += `
                            <div class="team-card">
                                <img src="${time.image_url || 'https://via.placeholder.com/100'}" alt="${time.name}" class="team-logo">
                                <h3>${time.name}</h3>
                                <p class="team-country">${pais}</p>
                                <a href="/time/${time.id}" class="team-link">Ver Detalhes</a>
                            </div>
                        `;
                    });
                    html += '</div>';
                    searchResults.innerHTML = html;
                } else {
                    searchResults.innerHTML = '<p class="no-results">Nenhum time encontrado com esse nome</p>';
                }
            } catch (error) {
                console.error('Erro na busca:', error);
                searchResults.innerHTML = '<p class="error">Erro ao buscar times</p>';
            }
        }
    }
});
