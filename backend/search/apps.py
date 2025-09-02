from django.apps import AppConfig
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel, BartTokenizer, BartForConditionalGeneration, pipeline
from keybert import KeyBERT

class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'
    local_model_path = 'search/local_model'
    local_ChatGLM_path = '../search/data/chatglm3-6b'
    local_bart_path = '../search/data/bart-large-cnn'

    def ready(self):
        self.sentence_model = SentenceTransformer(self.local_model_path,device="cuda")
        self.llm_tokenizer = AutoTokenizer.from_pretrained(self.local_ChatGLM_path, trust_remote_code=True)
        self.llm_model = AutoModel.from_pretrained(self.local_ChatGLM_path, trust_remote_code=True).half().cuda().eval()
        self.kw_model = KeyBERT(model=self.sentence_model)
        self.bart_tokenizer = BartTokenizer.from_pretrained(self.local_bart_path)
        self.bart_model = BartForConditionalGeneration.from_pretrained(self.local_bart_path)
        self.summarizer = pipeline("summarization", model=self.bart_model, tokenizer=self.bart_tokenizer,device="cuda")