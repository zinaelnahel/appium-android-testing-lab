package com.zinaelnahel.qualitylab;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.text.InputType;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

public class MainActivity extends Activity {
    private static final String DEMO_EMAIL = "demo@example.com";
    private static final String DEMO_PASSWORD = "QualityLab123!";
    private LinearLayout content;
    private EditText emailInput;
    private EditText passwordInput;
    private EditText searchInput;
    private TextView loginError;
    private TextView searchResult;
    private TextView notificationStatus;
    private boolean notificationsEnabled = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        showLogin();
    }

    private void beginScreen(String title, String subtitle) {
        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setBackgroundColor(Color.rgb(246, 247, 251));

        content = new LinearLayout(this);
        content.setOrientation(LinearLayout.VERTICAL);
        content.setPadding(dp(24), dp(28), dp(24), dp(28));
        content.setGravity(Gravity.TOP);
        scroll.addView(content, new ScrollView.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT));
        setContentView(scroll);

        TextView heading = new TextView(this);
        heading.setText(title);
        heading.setTextColor(Color.rgb(29, 39, 68));
        heading.setTextSize(28);
        heading.setTypeface(null, 1);
        heading.setContentDescription("screen-title");
        content.addView(heading, params(0));

        TextView helper = new TextView(this);
        helper.setText(subtitle);
        helper.setTextColor(Color.rgb(93, 103, 126));
        helper.setTextSize(15);
        content.addView(helper, params(8));
    }

    private void showLogin() {
        beginScreen("QualityLab", "A small mobile app for reliable UI testing.");
        addLabel("Sign in to the demo workspace");
        emailInput = addInput("Email", "login-email", InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_EMAIL_ADDRESS);
        passwordInput = addInput("Password", "login-password", InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);
        loginError = addLabel("");
        loginError.setContentDescription("login-error");
        loginError.setVisibility(View.GONE);
        addButton("Sign in", "login-submit", this::submitLogin);
        addLabel("Demo account: demo@example.com");
    }

    private void submitLogin() {
        String email = emailInput.getText().toString().trim();
        String password = passwordInput.getText().toString();
        if (DEMO_EMAIL.equals(email) && DEMO_PASSWORD.equals(password)) {
            showHome();
        } else {
            loginError.setText("Email or password is incorrect.");
            loginError.setVisibility(View.VISIBLE);
        }
    }

    private void showHome() {
        beginScreen("Welcome, Demo Tester", "Your test workspace is ready.");
        addLabel("Choose a flow to explore.");
        addButton("Search", "home-search", this::showSearch);
        addButton("Settings", "home-settings", this::showSettings);
        addButton("Sign out", "home-sign-out", this::showLogin);
    }

    private void showSearch() {
        beginScreen("Search", "Find a topic in the demo knowledge base.");
        addButton("Back to home", "search-back", this::showHome);
        searchInput = addInput("Search topics", "search-query", InputType.TYPE_CLASS_TEXT);
        searchResult = addLabel("");
        searchResult.setContentDescription("search-result");
        searchResult.setVisibility(View.GONE);
        addButton("Search", "search-submit", this::runSearch);
    }

    private void runSearch() {
        String query = searchInput.getText().toString().trim();
        if (query.isEmpty()) {
            searchResult.setText("Enter a search term.");
        } else if (query.toLowerCase().contains("accessibility")) {
            searchResult.setText("Accessibility checklist: labels, contrast, and focus order.");
        } else {
            searchResult.setText("Results for: " + query);
        }
        searchResult.setVisibility(View.VISIBLE);
    }

    private void showSettings() {
        beginScreen("Settings", "Manage preferences for this demo account.");
        addButton("Back to home", "settings-back", this::showHome);
        notificationStatus = addLabel(notificationText());
        notificationStatus.setContentDescription("notifications-status");
        addButton("Toggle notifications", "settings-notifications-toggle", () -> {
            notificationsEnabled = !notificationsEnabled;
            notificationStatus.setText(notificationText());
        });
    }

    private String notificationText() {
        return notificationsEnabled ? "Notifications are on." : "Notifications are off.";
    }

    private EditText addInput(String hint, String accessibilityId, int inputType) {
        EditText input = new EditText(this);
        input.setSingleLine(true);
        input.setHint(hint);
        input.setInputType(inputType);
        input.setTextSize(16);
        input.setContentDescription(accessibilityId);
        content.addView(input, params(12));
        return input;
    }

    private TextView addLabel(String text) {
        TextView label = new TextView(this);
        label.setText(text);
        label.setTextColor(Color.rgb(49, 58, 81));
        label.setTextSize(16);
        content.addView(label, params(18));
        return label;
    }

    private void addButton(String text, String accessibilityId, Runnable action) {
        Button button = new Button(this);
        button.setText(text);
        button.setContentDescription(accessibilityId);
        button.setAllCaps(false);
        button.setTextSize(16);
        content.addView(button, params(14));
        button.setOnClickListener(view -> action.run());
    }

    private LinearLayout.LayoutParams params(int topMarginDp) {
        LinearLayout.LayoutParams layoutParams = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT);
        layoutParams.topMargin = dp(topMarginDp);
        return layoutParams;
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }
}
