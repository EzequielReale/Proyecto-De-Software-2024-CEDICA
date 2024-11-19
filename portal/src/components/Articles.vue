<template>
    <section id="articles">
        <h1 class="fw-bolder" style="text-align: center;">Noticias y Actividades</h1>
        <br>
        <div v-if="articles.length === 0" class="loading">Cargando artículos...</div>
        <div v-else class="articles-container">
            <div class="articles-grid">
                <div v-for="article in getArticles" :key="article.updated_at" class="article"
                    :class="{ 'article-expanded': expandedArticle === article.title }">
                    <h2>{{ article.title }}</h2>
                    <template v-if="expandedArticle === article.title">
                        <div class="article-metadata">
                            <div class="article-author">
                                <span class="metadata-label">Autor:</span>
                                {{ article.author }}
                            </div>
                            <div class="article-date">
                                <span class="metadata-label">Publicado:</span>
                                {{ formatDate(article.published_at) }}
                            </div>
                        </div>
                        <div class="article-summary">
                            {{ article.summary }}
                        </div>
                        <div class="article-content" v-html="renderMarkdown(article.content)"></div>
                        <button @click="collapseArticle" class="action-button collapse-button">
                            <span class="button-icon">▼</span>
                            Cerrar nota
                        </button>
                    </template>
                    <template v-else>
                        <p class="article-preview-summary">{{ article.summary }}</p>
                        <div class="article-preview-footer">
                            <p class="article-preview-date">{{ formatDate(article.published_at) }}</p>
                            <button @click="expandArticle(article.title)" class="action-button expand-button">
                                <span class="button-icon">▶</span>
                                Ver nota completa
                            </button>
                        </div>
                    </template>
                </div>
            </div>
            <div class="load-more-container">
                <button @click="loadMore" v-if="hasMore" class="load-more-button">
                    Cargar más
                </button>
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref, onMounted, computed, normalizeClass } from 'vue';
import axios from 'axios';
import { marked } from 'marked';

const articles = ref([]);
const page = ref(1);
const perPage = 9;
const total = ref(0);
const expandedArticle = ref(null);

const fetchArticles = async () => {
    try {
        const response = await axios.get(`https://admin-grupo04.proyecto2024.linti.unlp.edu.ar/api/articles?page=${page.value}&per_page=${perPage}`);
        articles.value.push(...response.data.data);
        total.value = response.data.total;
    } catch (error) {
        console.error('Error fetching articles:', error);
    }
};

const loadMore = () => {
    page.value += 1;
    fetchArticles();
};

const formatDate = (date) => {
    return new Date(date).toLocaleDateString();
};

const expandArticle = (articleTitle) => {
    expandedArticle.value = articleTitle;
};

const collapseArticle = () => {
    expandedArticle.value = null;
};

const renderMarkdown = (content) => {
    const normalizedContent = content.replace(/(\S)\s\*/g, '$1\n\n*'); // Esto agrega saltos de línea antes de cada lista
    return marked(normalizedContent); // Esto convierte el contenido en HTML con Markdown
};

const getArticles = computed(() => {
    return articles.value;
});

const hasMore = computed(() => {
    return articles.value.length < total.value;
});

onMounted(() => {
    fetchArticles();
});
</script>

<style scoped>
#articles {
    padding: 2rem;
    min-height: 100vh;
}

.articles-title {
    text-align: center;
    font-size: 2rem;
    color: #333;
    margin-bottom: 2rem;
}

.articles-container {
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
}

.articles-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    width: 100%;
}

.article {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    min-height: 200px;
    display: flex;
    flex-direction: column;
    position: relative;
}

.article:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.article-expanded {
    grid-column: 1 / -1;
    min-height: auto;
    transform: none !important;
}

.article h2 {
    color: #333;
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    border-bottom: 2px solid #e0e0e0;
    padding-bottom: 0.5rem;
}

.article-metadata {
    display: flex;
    gap: 2rem;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
    color: #666;
}

.metadata-label {
    font-weight: 600;
    color: #26a69a;
    margin-right: 0.5rem;
}

.article-summary {
    background-color: #f8f8f8;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    line-height: 1.6;
    color: #444;
}

.article-content {
    line-height: 1.8;
    color: #333;
    margin-bottom: 2rem;
}

.article-preview-summary {
    color: #666;
    line-height: 1.5;
    margin-bottom: 1rem;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.article-preview-footer {
    margin-top: auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.article-preview-date {
    color: #888;
    font-size: 0.9rem;
}

.action-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: all 0.2s ease;
}

.expand-button {
    background-color: #26a69a;
    color: white;
}

.expand-button:hover {
    background-color: #2bbbad;
}

.collapse-button {
    background-color: #e0e0e0;
    color: #333;
}

.collapse-button:hover {
    background-color: #d0d0d0;
}

.button-icon {
    font-size: 0.8rem;
}

.load-more-container {
    width: 100%;
    display: flex;
    justify-content: center;
    margin-top: 2rem;
}

.load-more-button {
    background-color: #26a69a;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.2s ease;
}

.load-more-button:hover {
    background-color: #2bbbad;
    transform: translateY(-2px);
}

.loading {
    text-align: center;
    padding: 2rem;
    color: #666;
    font-size: 1.1rem;
}

@media (max-width: 768px) {
    #articles {
        padding: 1rem;
    }

    .articles-grid {
        gap: 15px;
    }

    .article-metadata {
        flex-direction: column;
        gap: 0.5rem;
    }
}
</style>