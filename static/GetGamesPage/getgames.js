async function loadCompaniesAndGames() {
    const dropdown = document.getElementById('companyDropdown');
    const companyResponse = await fetch('/updategamestable');
    const companies = await companyResponse.json();
    companies.forEach(company => {
        const option = document.createElement('option');
        option.value = company.id;
        option.textContent = company.name;
        dropdown.appendChild(option);
    });
    dropdown.addEventListener('change', async () => {
        const selectedCompany = dropdown.value;
       
        if (selectedCompany) {
            const response = await fetch('/updategamestable', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ company_id: selectedCompany }),
            });

            const games = await response.json();
           
            const tableBody = document.getElementById('gamesTableBody');
            tableBody.innerHTML = '';

            if (games.length > 0) {
                games.forEach(game => {
                    const row = `
                        <tr>
                            <td>
                                <a href="#">
                                    <img src="/static/assets/charts.png" class="chart-icon" width="40px">
                                </a>
                            </td>
                            <td><img src="${game.icon}" alt="Game Icon" width="50" class="game-icon"> ${game.title}</td>
                            <td>${game.status}</td>
                            <td>${game.cpi}</td>
                            <td>${game.cvr}</td>
                            <td>${game.ctr}</td>
                        </tr>
                    `;
                    tableBody.innerHTML += row;
                });
            } else {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="6">No games available for this company.</td>
                    </tr>
                `;
            }
        }
    });
}
window.addEventListener('DOMContentLoaded', loadCompaniesAndGames);
