document.addEventListener("DOMContentLoaded", async () => {
    // Add Dev Bypass Listener
    document.getElementById("devBypassBtn").addEventListener("click", () => {
        document.getElementById("app").style.display = "block";
        document.getElementById("sign-in-container").style.display = "none";
        initApp();
    });

    // Wait for Clerk to be loaded from CDN
    const checkClerk = setInterval(async () => {
        if (window.Clerk) {
            clearInterval(checkClerk);
            await initializeClerk();
        }
    }, 100);
});

async function initializeClerk() {
    try {
        await window.Clerk.load();
        
        if (window.Clerk.user) {
            // User is signed in
            document.getElementById("app").style.display = "block";
            document.getElementById("sign-in-container").style.display = "none";
            
            const userButtonDiv = document.getElementById("user-button");
            window.Clerk.mountUserButton(userButtonDiv);
            
            // Initialize app logic
            initApp();
        } else {
            // User is not signed in
            document.getElementById("app").style.display = "none";
            document.getElementById("sign-in-container").style.display = "flex";
            
            const signInDiv = document.getElementById("sign-in");
            window.Clerk.mountSignIn(signInDiv);
        }
    } catch (err) {
        console.error("Error initializing Clerk (You probably need to set a valid publishable key):", err);
        // Show the dev bypass button more prominently if Clerk fails to load
        document.getElementById("app").style.display = "none";
        document.getElementById("sign-in-container").style.display = "flex";
    }
}

function initApp() {
    const uploadForm = document.getElementById('upload-form');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loader = submitBtn.querySelector('.loader');
    const refreshBtn = document.getElementById('refreshBtn');

    // Load initial candidates
    fetchCandidates();

    refreshBtn.addEventListener('click', fetchCandidates);

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // UI Loading state
        submitBtn.disabled = true;
        btnText.style.display = 'none';
        loader.style.display = 'block';
        
        const formData = new FormData();
        formData.append('candidate_name', document.getElementById('candidateName').value);
        formData.append('candidate_email', document.getElementById('candidateEmail').value);
        formData.append('job_description', document.getElementById('jobDescription').value);
        formData.append('file', document.getElementById('cvFile').files[0]);

        try {
            const response = await fetch('http://localhost:8000/api/upload-cv/', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log('Success:', result);
            
            // Save to localStorage
            const candidatesStr = localStorage.getItem('candidates');
            let candidates = candidatesStr ? JSON.parse(candidatesStr) : [];
            candidates.push(result);
            localStorage.setItem('candidates', JSON.stringify(candidates));
            
            // Reset form
            uploadForm.reset();
            
            // Refresh list
            fetchCandidates();
            
            alert(`Candidate processed! Score: ${result.score}`);
        } catch (error) {
            console.error('Error uploading CV:', error);
            alert('Failed to process candidate. Make sure the backend is running.');
        } finally {
            // Restore UI state
            submitBtn.disabled = false;
            btnText.style.display = 'block';
            loader.style.display = 'none';
        }
    });
}

function fetchCandidates() {
    try {
        const candidatesStr = localStorage.getItem('candidates');
        let candidates = candidatesStr ? JSON.parse(candidatesStr) : [];
        
        // Sort by score descending
        candidates.sort((a, b) => b.score - a.score);
        
        const tbody = document.getElementById('candidatesBody');
        tbody.innerHTML = '';
        
        candidates.forEach(candidate => {
            const tr = document.createElement('tr');
            
            // Determine score class
            let scoreClass = 'score-low';
            if (candidate.score >= 80) scoreClass = 'score-high';
            else if (candidate.score >= 50) scoreClass = 'score-medium';

            tr.innerHTML = `
                <td><strong>${candidate.name}</strong><br><small>${candidate.filename}</small></td>
                <td>${candidate.email}</td>
                <td><span class="score-badge ${scoreClass}">${candidate.score}/100</span></td>
                <td><span class="status-badge">${candidate.status}</span></td>
                <td style="max-width: 300px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${candidate.reasoning}">
                    ${candidate.reasoning}
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error fetching candidates:', error);
    }
}
