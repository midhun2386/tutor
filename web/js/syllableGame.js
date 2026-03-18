/**
 * Syllable Game Component - Pure JS implementation of the matching game.
 */
export class SyllableGame {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.currentBuild = [];
        this.targetWord = "";
        this.syllables = [];
        this.onCompleteCallback = null;
    }

    init(targetWord, syllables) {
        this.targetWord = targetWord.trim().toLowerCase();
        this.syllables = syllables;
        this.currentBuild = [];
        this.render();
    }

    render() {
        if (!this.container) return;
        this.container.innerHTML = "";

        const gameWrapper = document.createElement('div');
        gameWrapper.className = 'syllable-game';

        // Syllable Buttons
        const buttonGroup = document.createElement('div');
        buttonGroup.className = 'syllable-buttons';
        this.syllables.forEach((syl, index) => {
            const btn = document.createElement('button');
            btn.className = 'game-tile';
            btn.innerText = syl;
            btn.onclick = () => this.addSyllable(syl);
            buttonGroup.appendChild(btn);
        });

        // Current Progress
        const progressDisp = document.createElement('div');
        progressDisp.className = 'game-progress';
        progressDisp.innerHTML = `<strong>Current Progress:</strong> <code>${this.currentBuild.join('') || '...'}</code>`;

        // Controls
        const controls = document.createElement('div');
        controls.className = 'game-controls';
        controls.style.display = 'flex';
        controls.style.justifyContent = 'center';
        controls.style.gap = '1rem';
        
        const resetBtn = document.createElement('button');
        resetBtn.innerText = "Reset 🔄";
        resetBtn.className = 'cta-button secondary';
        resetBtn.onclick = () => {
            this.currentBuild = [];
            this.render();
        };

        gameWrapper.appendChild(buttonGroup);
        gameWrapper.appendChild(progressDisp);
        gameWrapper.appendChild(controls);
        controls.appendChild(resetBtn);

        this.container.appendChild(gameWrapper);

        this.checkWin();
    }

    addSyllable(syl) {
        this.currentBuild.push(syl);
        this.render();
    }

    triggerVictory() {
        const emojis = ['🎉', '✨', '🎊', '🚀', '🌟'];
        for (let i = 0; i < 30; i++) {
            const p = document.createElement('div');
            p.className = 'victory-particle';
            p.innerText = emojis[Math.floor(Math.random() * emojis.length)];
            p.style.left = Math.random() * 100 + 'vw';
            p.style.animationDelay = Math.random() * 2 + 's';
            document.body.appendChild(p);
            setTimeout(() => p.remove(), 4000);
        }
    }

    checkWin() {
        const build = this.currentBuild.join('').toLowerCase();
        if (build === this.targetWord) {
            this.triggerVictory();
            
            const successMsg = document.createElement('div');
            successMsg.className = 'game-success';
            successMsg.innerHTML = `
                <h3>🎉 Perfect! You built the word: <strong>${this.targetWord}</strong></h3>
                <button class="cta-button proceed-btn" id="btn-proceed-lesson">Proceed to Next Lesson ➡️</button>
            `;
            this.container.appendChild(successMsg);
            
            document.getElementById('btn-proceed-lesson').onclick = () => {
                if (this.onCompleteCallback) this.onCompleteCallback();
            };
        } else if (build.length >= this.targetWord.length) {
            const errorMsg = document.createElement('div');
            errorMsg.className = 'game-error';
            errorMsg.style.textAlign = 'center';
            errorMsg.style.marginTop = '1rem';
            errorMsg.style.color = '#ef4444';
            errorMsg.innerText = "Almost! Try resetting and matching the syllables in order.";
            this.container.appendChild(errorMsg);
        }
    }

    onComplete(callback) {
        this.onCompleteCallback = callback;
    }
}
