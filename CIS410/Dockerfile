# ============================================================
# Multi-Stage Docker Build — Production-Grade
# CIS 410 — Cloud & DevOps | Preston Furulie
# ============================================================
# Covers: multi-stage builds, layer caching, non-root user,
# health checks, security best practices, .dockerignore,
# minimal base image, and build arguments.
# ============================================================

# ── Stage 1: Dependencies ──────────────────────────────────
# Install only production dependencies in a separate stage
# to leverage Docker layer caching.

FROM node:20-alpine AS deps
WORKDIR /app

# Copy only package files first (cache bust only when deps change)
COPY package.json package-lock.json ./

# Install production dependencies only
RUN npm ci --omit=dev && npm cache clean --force


# ── Stage 2: Build ─────────────────────────────────────────
# Compile TypeScript, bundle assets, run build step.

FROM node:20-alpine AS builder
WORKDIR /app

# Install ALL dependencies (including devDependencies for build)
COPY package.json package-lock.json ./
RUN npm ci

# Copy source code
COPY tsconfig.json ./
COPY src/ ./src/
COPY prisma/ ./prisma/

# Generate Prisma client
RUN npx prisma generate

# Build the application
RUN npm run build

# Prune dev dependencies after build
RUN npm prune --omit=dev


# ── Stage 3: Production ───────────────────────────────────
# Minimal production image with only what's needed to run.

FROM node:20-alpine AS production

# Security: install security updates
RUN apk update && apk upgrade --no-cache && rm -rf /var/cache/apk/*

# Security: create non-root user and group
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

WORKDIR /app

# Copy production dependencies from deps stage
COPY --from=deps --chown=appuser:appgroup /app/node_modules ./node_modules

# Copy built application from builder stage
COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
COPY --from=builder --chown=appuser:appgroup /app/package.json ./
COPY --from=builder --chown=appuser:appgroup /app/prisma ./prisma
COPY --from=builder --chown=appuser:appgroup /app/node_modules/.prisma ./node_modules/.prisma

# Environment configuration
ENV NODE_ENV=production
ENV PORT=3000
ENV LOG_LEVEL=info

# Expose the application port
EXPOSE 3000

# Switch to non-root user (security best practice)
USER appuser

# Health check: verify the application is responding
# --interval: check every 30 seconds
# --timeout:  fail if no response in 3 seconds
# --start-period: grace period for startup (don't count failures)
# --retries: mark unhealthy after 3 consecutive failures
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

# Start the application
CMD ["node", "dist/server.js"]


# ── Build metadata (OCI labels) ────────────────────────────
LABEL org.opencontainers.image.title="Guitar Shop API"
LABEL org.opencontainers.image.description="REST API for Guitar Shop Inventory"
LABEL org.opencontainers.image.authors="Preston Furulie"
LABEL org.opencontainers.image.source="https://github.com/Personfu/Python"
LABEL org.opencontainers.image.version="1.0.0"
