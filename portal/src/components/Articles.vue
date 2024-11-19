<template>
    <section id="articles">
        <div v-if="articles.length === 0" class="loading">Cargando artículos...</div>
        <div v-else class="articles-container">
            <div class="articles-grid">
                <div v-for="article in getArticles" :key="article.updated_at" class="article">
                    <h2>{{ article.title }}</h2>
                    <p>{{ article.summary }}</p>
                    <p>Publicado: {{ formatDate(article.published_at) }}</p>
                    <a :href="articleLink(article)">Ver nota completa</a>
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
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const articles = ref([]);
const page = ref(1);
const perPage = 9;
const total = ref(0);

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

const articleLink = (article) => {
    //return `https://admin-grupo04.proyecto2024.linti.unlp.edu.ar/articles/${article.title.replace(/\s+/g, '-').toLowerCase()}`;
};

const getArticles = computed(() => {
    return articles.value
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
    background-color: #f5f5f5;
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
    transition: transform 0.2s ease-in-out;
    min-height: 200px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.article:hover {
    transform: translateY(-5px);
}

.article h2 {
    color: #333;
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.article p {
    color: #666;
    line-height: 1.5;
    margin-bottom: 1rem;
}

.article a {
    color: #26a69a;
    text-decoration: none;
    font-weight: 500;
    margin-top: auto;
}

.article a:hover {
    text-decoration: underline;
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
    padding: 10px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
}

.load-more-button:hover {
    background-color: #2bbbad;
}

.loading {
    text-align: center;
    padding: 2rem;
}

@media (max-width: 768px) {
    #articles {
        padding: 1rem;
    }
    
    .articles-grid {
        gap: 15px;
    }
}
</style>