"""Tracks app tests."""

from django.test import TestCase

from .factories import GenomeFactory, LabFactory
from .models import Genome, Lab

LAB_GENOMES = {
    'lab_A': [
        'genome_A',
        'genome_B',
    ],
    'lab_B': [
        'genome_C',
        'genome_D',
        'genome_E',
        'genome_F',
    ],
    'lab_C': [
        'genome_G',
    ],
}


class GenomesTestCase(TestCase):
    """Test logic associated with Genome model and views."""

    def setUp(self):
        """Populate DB."""
        for lab_name, genome_names in LAB_GENOMES.items():
            lab = LabFactory(name=lab_name)
            for name in genome_names:
                GenomeFactory(
                    lab=lab,
                    name=name,
                )

    def tearDown(self):
        """Drop database records."""
        Lab.objects.all().delete()

    def test_create_genomes(self):
        """Test that genome records were created correctly."""
        lab_names = sorted(LAB_GENOMES.keys())
        self.assertEqual(Lab.objects.count(), len(LAB_GENOMES))
        self.assertEqual(Genome.objects.count(), sum([
            len(genomes)
            for genomes in LAB_GENOMES.values()
        ]))
        lab_1 = Lab.objects.get(name=lab_names[0])
        self.assertEqual(lab_1.genome_set.count(),
                         len(LAB_GENOMES[lab_names[0]]))
        lab_1_genome_names = lab_1.genome_set.values_list('name', flat=True)
        self.assertIn(LAB_GENOMES[lab_names[0]][0], lab_1_genome_names)

    def test_api_genome_list(self):
        """Test genome list API."""
        expect_genomes_count = sum([
            len(genomes)
            for genomes in LAB_GENOMES.values()
        ])
        response = self.client.get('/genomes/api/genomes/')
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(data['genomes']),
            expect_genomes_count)

    def test_api_genome_list_lab(self):
        """Test genome list API."""
        query_labs = [list(LAB_GENOMES.keys())[0]]
        expect_genomes_count = sum([
            len(genomes)
            for lab, genomes in LAB_GENOMES.items()
            if lab in query_labs
        ])
        response = self.client.get('/genomes/api/genomes/',
                                   {'labs': ",".join(query_labs)})
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(data['genomes']),
            expect_genomes_count)
        self.assert_genome_names(query_labs, data)

    def test_api_genome_list_multiple_labs(self):
        """Test genome list API."""
        query_labs = list(LAB_GENOMES.keys())[:2]
        expect_genomes_count = sum([
            len(genomes)
            for lab, genomes in LAB_GENOMES.items()
            if lab in query_labs
        ])
        response = self.client.get('/genomes/api/genomes/',
                                   {'labs': ",".join(query_labs)})
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(data['genomes']),
            expect_genomes_count)
        self.assert_genome_names(query_labs, data)

    def assert_genome_names(self, query_labs, response_data):
        """Assert correct genomes in reponse data."""
        genome_names = {g['name'] for g in response_data['genomes']}
        expect_genome_names = {
            genome
            for lab, genomes in LAB_GENOMES.items()
            for genome in genomes
            if lab in query_labs
        }
        expect_not_genome_names = {
            genomes[0]
            for lab, genomes in LAB_GENOMES.items()
            if lab not in query_labs
        }
        self.assertEqual(genome_names, expect_genome_names)
        self.assertEqual(genome_names & expect_not_genome_names, set())
