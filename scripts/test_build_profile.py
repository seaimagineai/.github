"""Exercise project expansion without publishing placeholder repositories."""
import copy
import unittest
from unittest.mock import patch
import build_profile as builder

class ProjectExpansionTests(unittest.TestCase):
    def setUp(self):
        self.copy = copy.deepcopy(builder.COPY)
        self.projects = copy.deepcopy(builder.PROJECTS)

    def test_non_model_project_without_image_or_website(self):
        project = {'id':'test-tool','title':'Test tool','repository':'test-tool','category':'tools'}
        self.copy['en']['projects']['test-tool'] = {'description':'A tool description.','audience':'Developers.'}
        self.copy['en']['categories']['tools'] = {'title':'Tools','intro':'Utilities for a task.'}
        with patch.object(builder,'COPY',self.copy), patch.object(builder,'PROJECTS',self.projects+[project]), patch.object(builder,'CATEGORIES',builder.CATEGORIES+['tools']):
            result=builder.render('en')
        section=result.split('#### [Test tool]')[1].split('## ')[0]
        self.assertIn('A tool description.',section)
        self.assertNotIn('Create with this model',section)
        self.assertNotIn('/assets/',section)
        self.assertIn('### Tools',result)

    def test_project_reordering_keeps_copy_with_its_id(self):
        reversed_projects=list(reversed(self.projects))
        with patch.object(builder,'PROJECTS',reversed_projects):
            result=builder.render('en')
        self.assertLess(result.index('#### [Seedance'),result.index('#### [Gemini'))
        section=result.split('#### [Seedance')[1].split('#### ')[0]
        self.assertIn(builder.COPY['en']['projects']['seedance']['description'],section)
        self.assertNotIn(builder.COPY['en']['projects']['gemini-omni']['description'],section)

    def test_missing_locale_uses_explicit_english_readme(self):
        project={'repository':'test-tool','readmes':{'en':'docs/README.md'}}
        self.assertEqual(builder.project_link(project,'cn'),'https://github.com/seaimagineai/test-tool/blob/main/docs/README.md')

    def test_empty_category_is_not_rendered(self):
        with patch.object(builder,'CATEGORIES',builder.CATEGORIES+['unpublished']):
            result=builder.render('en')
        self.assertNotIn('unpublished',result)

if __name__ == '__main__':unittest.main()
