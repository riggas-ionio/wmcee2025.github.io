# frozen_string_literal: true

source "https://rubygems.org"

gem "github-pages", "~> 228", group: :jekyll_plugins

group :test do
  gem "html-proofer", "~> 3.18"
end

platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "wdm", "~> 0.1.1", platforms: [:mingw, :x64_mingw, :mswin]
gem "http_parser.rb", "~> 0.6.0", platforms: [:jruby]