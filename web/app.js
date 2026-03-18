import * as THREE from 'three';
import { API } from './js/api.js';
import { Recorder } from './js/recorder.js';
import { SyllableGame } from './js/syllableGame.js';

/**
 * AVA AI - Main Application Controller
 */
class App {
    constructor() {
        this.state = {
            studentId: null,
            studentName: '',
            language: 'tamil',
            proficiency: 'Beginner',
            sessionId: null,
            lessonsCompleted: 0,
            currentLesson: null,
            excludedTexts: [],
            quizMode: false
        };

        this.recorder = new Recorder();
        this.game = new SyllableGame('game-mount');
        this.crystal = null;
        
        this.init();
    }

    async init() {
        this.initThree();
        this.bindEvents();
        await this.loadProfiles();
        await this.recorder.init();
    }

    // ── 3D Scene Initialization ──────────────────────────────────────────────
    initThree() {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        document.getElementById('canvas-container').appendChild(renderer.domElement);

    // Particle System (Nebula)
    const particlesCount = 2000;
    const posArray = new Float32Array(particlesCount * 3);
    
    for(let i=0; i < particlesCount * 3; i++) {
        posArray[i] = (Math.random() - 0.5) * 15;
    }

    const particlesGeometry = new THREE.BufferGeometry();
    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.02,
        color: 0x6366f1,
        transparent: true,
        opacity: 0.8,
        blending: THREE.AdditiveBlending
    });

    const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particlesMesh);
    this.particles = particlesMesh;

    scene.add(new THREE.AmbientLight(0xffffff, 0.5));
    
    camera.position.z = 5;

    const animate = () => {
        requestAnimationFrame(animate);
        this.particles.rotation.y += 0.001;
        this.particles.rotation.x += 0.0005;
        
        // Subtle wave motion
        const time = Date.now() * 0.0005;
        this.particles.position.y = Math.sin(time) * 0.1;
        
        renderer.render(scene, camera);
    };

    animate();

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    document.addEventListener('mousemove', (e) => {
        const mouseX = (e.clientX / window.innerWidth) * 2 - 1;
        const mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
        this.particles.rotation.y += mouseX * 0.05;
        this.particles.rotation.x += mouseY * 0.05;
    });
}

    // ── Event Bindings & Routing ─────────────────────────────────────────────
    bindEvents() {
        // Navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.onclick = () => {
                const view = btn.dataset.view;
                this.switchView(view);
                if (view === 'progress') this.loadProgress();
            };
        });

        // Profile Selection
        const studentSelect = document.getElementById('student-select');
        const btnContinue = document.getElementById('btn-continue');
        const btnDelete = document.getElementById('btn-delete-profile');

        studentSelect.onchange = () => {
            const val = studentSelect.value;
            btnContinue.disabled = !val;
            
            if (val) {
                btnDelete.classList.remove('hidden');
                const opt = studentSelect.options[studentSelect.selectedIndex];
                this.state.studentId = val;
                this.state.studentName = opt.text;
                this.state.language = opt.dataset.lang;
                this.state.proficiency = opt.dataset.level;
            } else {
                btnDelete.classList.add('hidden');
                this.state.studentId = null;
            }
        };

        btnContinue.onclick = () => this.startSession();

        btnDelete.onclick = async () => {
            if (!this.state.studentId) return;
            
            const confirmMsg = `Are you sure you want to permanently delete the profile for "${this.state.studentName}"?\n\nThis will completely wipe all of their learning progress, history, and phonetic mastery scores. This cannot be undone.`;
            
            if (confirm(confirmMsg)) {
                try {
                    btnDelete.innerText = '⏳ Deleting...';
                    await API.deleteStudent(this.state.studentId);
                    this.notify("Profile deleted successfully.", "info");
                    
                    // Reset UI
                    btnDelete.classList.add('hidden');
                    btnContinue.disabled = true;
                    this.state.studentId = null;
                    
                    // Reload the profile list
                    await this.loadProfiles();
                } catch (err) {
                    this.notify(`Failed to delete profile: ${err.message}`, "error");
                } finally {
                    btnDelete.innerText = '🗑️ Delete';
                }
            }
        };

        // Registration form
        document.getElementById('registration-form').onsubmit = async (e) => {
            e.preventDefault();
            const name = document.getElementById('reg-name').value;
            const lang = document.getElementById('reg-lang').value;
            const level = document.getElementById('reg-level').value;
            
            const student = await API.createStudent(name, lang, level);
            if (student.id) {
                this.state.studentId = student.id;
                this.state.studentName = student.name;
                this.state.language = student.language;
                this.state.proficiency = student.proficiency_level;
                await this.startSession();
            }
        };

        // Lesson flow
        document.getElementById('btn-record').onclick = () => this.toggleRecording();
        document.getElementById('btn-next-lesson').onclick = () => this.getNextLesson();
        document.getElementById('btn-start-quiz').onclick = () => this.startQuiz();
        document.getElementById('btn-speak').onclick = () => this.speakLesson();
    }

    switchView(viewId) {
        document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        
        document.getElementById(`view-${viewId}`).classList.add('active');
        document.querySelector(`.nav-btn[data-view="${viewId}"]`).classList.add('active');
    }

    // ── Business Logic ───────────────────────────────────────────────────────
    async loadProfiles() {
        const students = await API.getStudents();
        const select = document.getElementById('student-select');
        
        // Clear existing options except the placeholder
        select.innerHTML = '<option value="">-- Select Profile --</option>';

        students.forEach(s => {
            const opt = document.createElement('option');
            opt.value = s.id;
            opt.text = s.name;
            opt.dataset.lang = s.language;
            opt.dataset.level = s.proficiency_level;
            select.appendChild(opt);
        });
    }

    async startSession() {
        const session = await API.startSession(this.state.studentId);
        this.state.sessionId = session.session_id;
        
        document.getElementById('nav-lesson').disabled = false;
        document.getElementById('nav-progress').disabled = false;
        document.getElementById('session-info').innerHTML = `<p>👤 <strong>${this.state.studentName}</strong></p><p>Level: ${this.state.proficiency}</p>`;
        
        await this.loadProgress();
        this.switchView('lesson');
        this.getNextLesson();
    }

    async loadProgress() {
        console.log("Loading progress for student:", this.state.studentId);
        try {
            if (!this.state.studentId) {
                console.warn("No student ID set, cannot load progress.");
                return;
            }
            const data = await API.getStudent(this.state.studentId);
            console.log("Progress data received:", data);
            
            // Try new ID first, fallback to old ID for backward compatibility
            let grid = document.getElementById('progress-grid') || document.getElementById('stats-grid');
            
            if (!grid) {
                console.error("Progress container (progress-grid or stats-grid) not found!");
                return;
            }
            
            const html = data.phoneme_progress.map(p => `
                <div class="progress-card">
                    <h4>${p.phoneme}</h4>
                    <div class="mastery-bar">
                        <div class="mastery-fill" style="width: ${p.mastery_score * 100}%"></div>
                    </div>
                    <span>Mastery: ${(p.mastery_score * 100).toFixed(0)}%</span>
                </div>
            `).join('');

            grid.innerHTML = html || '<p class="empty-msg">Start lessons to see your progress!</p>';
        } catch (err) {
            console.error("Failed to load progress:", err);
            this.notify("Could not load progress journey.", "error");
        }
    }

    async getNextLesson() {
        try {
            this.state.quizMode = false;
            document.getElementById('analysis-results').classList.add('hidden');
            document.getElementById('quiz-container').classList.add('hidden');
            
            const lesson = await API.generateLesson(
                this.state.studentId, 
                this.state.language, 
                this.state.lastEmotion || 'Confident', 
                this.state.proficiency,
                this.state.excludedTexts
            );
            
            this.state.currentLesson = lesson;
            // Add to excluded list so we don't see it again soon
            if (lesson.lesson_text && !this.state.excludedTexts.includes(lesson.lesson_text)) {
                this.state.excludedTexts.push(lesson.lesson_text);
            }

            document.getElementById('lesson-text').innerText = lesson.lesson_text;
            document.getElementById('lesson-hint').innerHTML = `<i>Hint: ${lesson.hint}</i>`;
        } catch (err) {
            this.notify(`Failed to fetch lesson: ${err.message}`, 'error');
        }
    }

    toggleRecording() {
        const btn = document.getElementById('btn-record');
        if (this.recorder.isRecording) {
            this.recorder.stop();
            btn.innerText = "🎙️ Start Recording";
            btn.classList.remove('recording');
        } else {
            this.recorder.onStop(blob => this.processAudio(blob));
            this.recorder.start();
            btn.innerText = "🛑 Stop Recording";
            btn.classList.add('recording');
        }
    }

    async processAudio(blob) {
        const btn = document.getElementById('btn-record');
        btn.disabled = true;
        btn.innerText = "⏳ Analyzing...";

        try {
            const analysis = await API.analyzeAudio(
                blob, 
                this.state.language, 
                this.state.sessionId, 
                this.state.currentLesson.lesson_text
            );
            
            this.state.lastEmotion = analysis.emotion_label;
            this.displayAnalysis(analysis);
            this.speakFeedback(analysis.creative_feedback);
        } catch (err) {
            this.notify(`Analysis error: ${err.message}`, 'error');
        } finally {
            btn.disabled = false;
            btn.innerText = "🎙️ Start Recording";
        }
    }

    notify(message, type = 'info') {
        const area = document.getElementById('notification-area');
        const note = document.createElement('div');
        note.className = `notification ${type}`;
        note.innerText = message;
        area.appendChild(note);
        setTimeout(() => note.remove(), 5000);
    }

    displayAnalysis(data) {
        const panel = document.getElementById('analysis-results');
        panel.classList.remove('hidden');
        
        document.getElementById('transcript-text').innerHTML = `I heard: <strong>${data.transcript}</strong>`;
        document.getElementById('emotion-label').innerHTML = `Emotion: <strong>${data.emotion_label}</strong> (${(data.confidence * 100).toFixed(1)}%)`;
        
        this.state.lessonsCompleted++;
        const pct = (this.state.lessonsCompleted / 3) * 100;
        document.getElementById('progress-bar-fill').style.width = `${Math.min(pct, 100)}%`;
        document.getElementById('progress-text').innerText = `${Math.min(this.state.lessonsCompleted, 3)}/3 lessons completed`;
        
        if (this.state.lessonsCompleted >= 3) {
            document.getElementById('btn-next-lesson').classList.add('hidden');
            document.getElementById('btn-start-quiz').classList.remove('hidden');
        } else {
            document.getElementById('btn-next-lesson').classList.remove('hidden');
            document.getElementById('btn-start-quiz').classList.add('hidden');
        }
    }

    speakLesson() {
        const utterance = new SpeechSynthesisUtterance(this.state.currentLesson.lesson_text);
        utterance.lang = this.state.language === 'tamil' ? 'ta-IN' : (this.state.language === 'hindi' ? 'hi-IN' : 'en-US');
        window.speechSynthesis.speak(utterance);
    }

    speakFeedback(text) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = this.state.language === 'tamil' ? 'ta-IN' : (this.state.language === 'hindi' ? 'hi-IN' : 'en-US');
        window.speechSynthesis.speak(utterance);
    }

    startQuiz() {
        document.getElementById('quiz-container').classList.remove('hidden');
        const lesson = this.state.currentLesson;
        this.game.init(lesson.target_word || lesson.lesson_text, lesson.syllables || []);
        this.game.onComplete(async () => {
            console.log("Quiz complete callback triggered. Phoneme:", lesson.phoneme);
            try {
                // Update persistent progress in DB
                if (lesson.phoneme) {
                    const result = await API.updateProgress(this.state.studentId, lesson.phoneme, true);
                    console.log("Progress update result:", result);
                    this.notify("Mastery Updated! 🌟", "info");
                    await this.loadProgress();
                } else {
                    console.warn("No phoneme associated with this lesson, skip progress update.");
                }
                this.state.lessonsCompleted = 0;
                this.getNextLesson();
            } catch (err) {
                console.error("Progress update failed:", err);
                this.state.lessonsCompleted = 0; 
                this.getNextLesson();
            }
        });
    }
}

// Start the app when the page loads
window.onload = () => new App();
