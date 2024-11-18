from marshmallow import Schema, fields,validate,pre_dump
import re

class ArticleSchema(Schema):
    title = fields.Str(required=True,dump_only=True) #dump_only para que no lo puedan cambiar en un post
    summary = fields.Str(required=True,dump_only=True)
    content = fields.Str(required=True,dump_only=True)
    published_at = fields.DateTime(required=True,dump_only=True,format='%Y-%m-%dT%H:%M:%SZ')
    updated_at = fields.DateTime(required=True,dump_only=True,format='%Y-%m-%dT%H:%M:%SZ')
    author = fields.Method("get_author_alias",dump_only=True)
    def get_author_alias(self, obj):
        return obj.author.alias if obj.author else None
    status = fields.Method("get_status",required=True,dump_only=True)
    def get_status(self,obj):
        return obj.status.name if obj.status else None
    
    @pre_dump 
    def clean_fields(self, obj, **kwargs): 
        if obj.summary:
            obj.summary = re.sub(r'\s+', ' ', obj.summary).strip() 
        if obj.content: 
            obj.content = re.sub(r'^[#\s]+', '', obj.content).strip() 
            obj.content = re.sub(r'\s+', ' ', obj.content).strip() 
        return obj

class ArticleFilterSchema(Schema):
    author = fields.Str(required=False) 
    published_from = fields.DateTime(required=False) 
    published_to = fields.DateTime(required=False) 
    page = fields.Integer(required=False, validate=validate.Range(min=1)) 
    per_page = fields.Integer(required=False, validate=validate.Range(min=1, max=100)) 


article_schema = ArticleSchema() 
articles_schema = ArticleSchema(many=True) # para varios 
article_filter_schema = ArticleFilterSchema()