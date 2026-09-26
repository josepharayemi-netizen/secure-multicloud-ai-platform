output "cluster_name" {value = module.eks.cluster_name}
output "artifact_bucket" {value = aws_s3_bucket.artifacts.id}
output "registry_url" {value = aws_ecr_repository.api.repository_url}
