/**
 * API Client for communication with the FastAPI backend.
 */
export class API {
    static BASE_URL = 'http://127.0.0.1:8000';

    static async getHealth() {
        const res = await fetch(`${this.BASE_URL}/api/health`);
        return res.json();
    }

    static async getStudents() {
        const res = await fetch(`${this.BASE_URL}/student/`);
        return res.json();
    }

    static async getStudent(studentId) {
        const res = await fetch(`${this.BASE_URL}/student/${studentId}`);
        return res.json();
    }

    static async createStudent(name, language, proficiency_level) {
        const res = await fetch(`${this.BASE_URL}/student/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, language, proficiency_level })
        });
        return res.json();
    }

    static async deleteStudent(studentId) {
        const res = await fetch(`${this.BASE_URL}/student/${studentId}`, {
            method: 'DELETE'
        });
        if (!res.ok) {
            throw new Error(`Failed to delete profile (${res.status})`);
        }
        return true;
    }

    static async startSession(studentId) {
        const res = await fetch(`${this.BASE_URL}/student/${studentId}/session/start`, {
            method: 'POST'
        });
        return res.json();
    }

    static async generateLesson(studentId, language, emotion, proficiency, excludedTexts = []) {
        const res = await fetch(`${this.BASE_URL}/lessons/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                student_id: studentId,
                language: language,
                emotion: emotion,
                proficiency_level: proficiency,
                excluded_texts: excludedTexts
            })
        });
        return res.json();
    }

    static async updateProgress(studentId, phoneme, correct) {
        const res = await fetch(`${this.BASE_URL}/student/${studentId}/progress`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phoneme, correct })
        });
        return res.json();
    }

    static async analyzeAudio(audioBlob, language, session_id, expected_text) {
        const formData = new FormData();
        formData.append('file', audioBlob, 'audio.wav');
        formData.append('language', language);
        formData.append('session_id', session_id);
        formData.append('expected_text', expected_text);

        const res = await fetch(`${this.BASE_URL}/audio/analyze`, {
            method: 'POST',
            body: formData
        });
        
        if (!res.ok) {
            const errBody = await res.json().catch(() => ({}));
            throw new Error(errBody.detail || `Analysis failed (${res.status})`);
        }
        
        return res.json();
    }
}
