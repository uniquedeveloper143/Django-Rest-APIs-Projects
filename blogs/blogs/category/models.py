from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Category(TimeStampedModel):
    title = models.CharField(_("Title"), max_length=200, help_text="The category title.")
    meta_title = models.TextField(_('Meta title'), null=True, blank=True,
                                  help_text="The meta title to be used for browser title and SEO.")
    slug = models.SlugField(_('Slug'), max_length=250, null=True, blank=True)
    content = models.TextField(_("Category content"), null=True, blank=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
