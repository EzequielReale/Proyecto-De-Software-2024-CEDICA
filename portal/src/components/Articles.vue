<template>
    <section id="articles" class="d-flex justify-content-center align-items-center" style="height: 100vh; width: 100%;">
        <div v-if="articles.length === 0">Cargando artículos...</div>
        <div v-else>
            <div v-for="article in sortedArticles" :key="article.updated_at" class="article">
                <h2>{{ article.title }}</h2>
                <p>{{ article.summary }}</p>
                <p>Publicado: {{ formatDate(article.published_at) }}</p>
                <a :href="articleLink(article)">Ver nota completa</a>
            </div>
            <button @click="loadMore" v-if="hasMore">Cargar más</button>
        </div>
    </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const articles = ref([]);
const page = ref(1);
const perPage = 10;
const total = ref(0);

const fetchArticles = async () => {
    try {
        const response = await axios.get(`https://admin-grupo04.proyecto2024.linti.unlp.edu.ar/api/articles`);
        articles.value.push(...response.data.data);
        total.value = response.data.total;
    } catch (error) {
        console.error('Error fetching articles:', error);
    }
};

const loadMore = () => {
    page.value += 10;
    fetchArticles();
};

const formatDate = (date) => {
    if (!date) return 'No publicada';
    return new Date(date).toLocaleDateString();
};

const articleLink = (article) => {
    return `https://admin-grupo04.proyecto2024.linti.unlp.edu.ar/articles/${article.title.replace(/\s+/g, '-').toLowerCase()}`;
};

const sortedArticles = computed(() => {
    return articles.value.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
});

const hasMore = computed(() => {
    return articles.value.length < total.value;
});

onMounted(() => {
    fetchArticles();
});
</script>

<style scoped>
.article {
    margin-bottom: 20px;
}
</style>