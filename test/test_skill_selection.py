import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

module_path = Path(__file__).parents[1] / 'backend/open_webui/utils/skill_selection.py'
module_spec = spec_from_file_location('skill_selection', module_path)
assert module_spec is not None and module_spec.loader is not None
skill_selection = module_from_spec(module_spec)
module_spec.loader.exec_module(skill_selection)
resolve_skill_ids = skill_selection.resolve_skill_ids


class ResolveSkillIdsTest(unittest.TestCase):
    def test_model_defaults_remain_description_only_when_submitted_by_the_client(self):
        user, available = resolve_skill_ids(
            ['coolify', 'onecli-google'],
            ['coolify', 'onecli-google'],
            [],
        )

        self.assertEqual(user, set())
        self.assertEqual(available, {'coolify', 'onecli-google'})

    def test_non_default_selection_requests_full_skill_content(self):
        user, available = resolve_skill_ids(
            ['coolify', 'pdf-editor'],
            ['coolify'],
            [],
        )

        self.assertEqual(user, {'pdf-editor'})
        self.assertEqual(available, {'coolify', 'pdf-editor'})

    def test_explicit_mention_promotes_a_model_default_to_full_content(self):
        user, available = resolve_skill_ids(
            ['coolify'],
            ['coolify'],
            ['coolify'],
        )

        self.assertEqual(user, {'coolify'})
        self.assertEqual(available, {'coolify'})


if __name__ == '__main__':
    unittest.main()
